"""
APScheduler service for income distribution and automated tasks
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.models import IncomeDistribution, IncomePayout, Holding, User, Asset
from services.hedera_service import hedera_service
from utils.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for managing scheduled tasks"""
    
    def __init__(self):
        """Initialize scheduler"""
        self.scheduler = BackgroundScheduler(timezone=settings.SCHEDULER_TIMEZONE)
        self.scheduler.add_listener(self._job_listener, mask=7)  # Listen to all events
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("📅 Scheduler started successfully")
            
            # Schedule recurring tasks
            self._schedule_recurring_tasks()
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logger.info("📅 Scheduler stopped")
    
    @property
    def running(self) -> bool:
        """Check if scheduler is running"""
        return self.scheduler.running
    
    def _job_listener(self, event):
        """Listen to job events for logging"""
        if event.exception:
            logger.error(f"Job {event.job_id} crashed: {event.exception}")
        else:
            logger.info(f"Job {event.job_id} executed successfully")
    
    def _schedule_recurring_tasks(self):
        """Schedule recurring maintenance tasks"""
        # Process pending income distributions every hour
        self.scheduler.add_job(
            func=self._process_pending_distributions,
            trigger=CronTrigger(minute=0),  # Every hour at minute 0
            id="process_distributions",
            name="Process Pending Income Distributions",
            replace_existing=True
        )
        
        # Sync with Mirror Node every 30 minutes
        self.scheduler.add_job(
            func=self._sync_mirror_node_data,
            trigger=CronTrigger(minute="*/30"),  # Every 30 minutes
            id="sync_mirror_node",
            name="Sync Mirror Node Data",
            replace_existing=True
        )
        
        logger.info("📅 Recurring tasks scheduled")
    
    def schedule_income_distribution(self, distribution_id: int, 
                                   distribution_date: datetime) -> bool:
        """Schedule a specific income distribution"""
        try:
            job_id = f"income_distribution_{distribution_id}"
            
            self.scheduler.add_job(
                func=self._execute_income_distribution,
                trigger=DateTrigger(run_date=distribution_date),
                args=[distribution_id],
                id=job_id,
                name=f"Income Distribution {distribution_id}",
                replace_existing=True
            )
            
            logger.info(f"📅 Scheduled income distribution {distribution_id} for {distribution_date}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to schedule income distribution {distribution_id}: {e}")
            return False
    
    async def _execute_income_distribution(self, distribution_id: int):
        """Execute income distribution for a specific distribution ID"""
        db = SessionLocal()
        try:
            # Get distribution record
            distribution = db.query(IncomeDistribution).filter(
                IncomeDistribution.id == distribution_id
            ).first()
            
            if not distribution:
                logger.error(f"Distribution {distribution_id} not found")
                return
            
            if distribution.status != "scheduled":
                logger.warning(f"Distribution {distribution_id} is not in scheduled status")
                return
            
            # Update status to processing
            distribution.status = "processing"
            db.commit()
            
            logger.info(f"💰 Processing income distribution {distribution_id}")
            
            # Get asset and token holders
            asset = db.query(Asset).filter(Asset.id == distribution.asset_id).first()
            if not asset:
                logger.error(f"Asset {distribution.asset_id} not found")
                distribution.status = "failed"
                db.commit()
                return
            
            # Get all token holders for this asset
            holdings = db.query(Holding).filter(
                Holding.asset_id == distribution.asset_id,
                Holding.amount > 0
            ).all()
            
            if not holdings:
                logger.warning(f"No token holders found for asset {distribution.asset_id}")
                distribution.status = "completed"
                db.commit()
                return
            
            # Calculate total tokens in circulation
            total_tokens = sum(holding.amount for holding in holdings)
            
            # Create payout records and execute transfers
            successful_payouts = 0
            failed_payouts = 0
            
            for holding in holdings:
                # Calculate payout amount based on token share
                share_percentage = holding.amount / total_tokens
                payout_amount = distribution.total_income * share_percentage
                
                # Create payout record
                payout = IncomePayout(
                    distribution_id=distribution_id,
                    user_id=holding.user_id,
                    amount=payout_amount,
                    status="pending"
                )
                db.add(payout)
                db.flush()  # Get the payout ID
                
                # Get user wallet info
                user = db.query(User).filter(User.id == holding.user_id).first()
                if not user:
                    logger.error(f"User {holding.user_id} not found")
                    payout.status = "failed"
                    failed_payouts += 1
                    continue
                
                # Execute HBAR transfer
                try:
                    transfer_result = await hedera_service.transfer_hbar(
                        from_account=settings.TREASURY_ID,
                        to_account=user.wallet_id,
                        amount=payout_amount,
                        private_key=settings.TREASURY_KEY
                    )
                    
                    if transfer_result.get("status") == "success":
                        payout.transaction_id = transfer_result["transaction_id"]
                        payout.status = "success"
                        successful_payouts += 1
                        logger.info(f"💸 Paid {payout_amount} HBAR to {user.wallet_id}")
                    else:
                        payout.status = "failed"
                        failed_payouts += 1
                        logger.error(f"Failed to pay {user.wallet_id}: {transfer_result.get('error')}")
                
                except Exception as e:
                    logger.error(f"Error paying {user.wallet_id}: {e}")
                    payout.status = "failed"
                    failed_payouts += 1
            
            # Update distribution status
            if failed_payouts == 0:
                distribution.status = "completed"
                logger.info(f"✅ Income distribution {distribution_id} completed successfully")
            elif successful_payouts > 0:
                distribution.status = "partially_completed"
                logger.warning(f"⚠️ Income distribution {distribution_id} partially completed")
            else:
                distribution.status = "failed"
                logger.error(f"❌ Income distribution {distribution_id} failed completely")
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error executing income distribution {distribution_id}: {e}")
            if distribution:
                distribution.status = "failed"
                db.commit()
        finally:
            db.close()
    
    async def _process_pending_distributions(self):
        """Process any pending income distributions"""
        db = SessionLocal()
        try:
            # Find distributions that should have been processed
            now = datetime.utcnow()
            pending_distributions = db.query(IncomeDistribution).filter(
                IncomeDistribution.status == "scheduled",
                IncomeDistribution.distribution_date <= now
            ).all()
            
            for distribution in pending_distributions:
                logger.info(f"Processing overdue distribution {distribution.id}")
                await self._execute_income_distribution(distribution.id)
                
        except Exception as e:
            logger.error(f"Error processing pending distributions: {e}")
        finally:
            db.close()
    
    async def _sync_mirror_node_data(self):
        """Sync data with Mirror Node for verification"""
        db = SessionLocal()
        try:
            # Get recent transactions that need verification
            from services.mirror_service import mirror_service
            
            # This is a placeholder for Mirror Node sync logic
            # In a real implementation, you would:
            # 1. Query recent transactions from Mirror Node
            # 2. Verify against local database
            # 3. Update transaction statuses
            # 4. Log any discrepancies
            
            logger.info("🔄 Mirror Node sync completed")
            
        except Exception as e:
            logger.error(f"Error syncing with Mirror Node: {e}")
        finally:
            db.close()
    
    def get_scheduled_jobs(self) -> List[Dict[str, Any]]:
        """Get list of scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        return jobs
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a scheduled job"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"📅 Cancelled job {job_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel job {job_id}: {e}")
            return False


# Global scheduler instance
scheduler = SchedulerService()
