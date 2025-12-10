from enum import Enum
from datetime import datetime
from abc import abstractmethod, ABC
import uuid

class JobType(Enum):
    BATCH = 'batch'
    REALTIME = 'realtime'

class JobProcessor(ABC):
    @abstractmethod
    def process_job(self, job):
        pass

class BatchJobProcessor(JobProcessor):
    def process_job(self, job):
        # custom logic to process jobs in batch, will be filled later
        return True
    
class RealTimeJobProcessor(JobProcessor):
    def process_job(self, job):
        # custom logic to process jobs in real time, will be filled later
        return True

class Job:
    def __init__(self, job_data: str, job_type: JobType):
        self.id = uuid.uuid4()
        self.job_data = job_data
        self.job_type = job_type
        self.created = datetime.now()
    
class JobScheduler:
    def __init__(self):
        self.jobs = {}
        self.id = uuid.uuid4()
        self.rtjp = RealTimeJobProcessor()
        self.bjp = BatchJobProcessor()

    def create_job(self, job_data, job_type):
        new_job = Job(job_data=job_data, job_type=job_type)
        self.jobs[new_job.id] = new_job
        return new_job.id
    
    def process_job(self, job_id):
        if job_id in self.jobs:
            curr_job = self.jobs[job_id]
            if curr_job.job_type == JobType.BATCH:
                return self.bjp.process_job(curr_job)
            else:
                return self.rtjp.process_job(curr_job)
        return False
    
if __name__ == '__main__':
    js1 = JobScheduler()
    j1_id = js1.create_job('clean logs', JobType.BATCH)
    j2_id = js1.create_job('send alert', JobType.REALTIME)
    print(js1.process_job(j1_id))
    print(js1.process_job(j2_id))
    print(js1.jobs)