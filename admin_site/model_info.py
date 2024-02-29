TEMPORAL_STATUS = (
    ('pending', 'PENDING'), ('completed', 'COMPLETED')
)

CONFIRMATION_STATUS = (
    ('pending', 'PENDING'), ('confirmed', 'CONFIRMED')
)

LOAN_REFUND_TYPE = (
    ('salary', 'NEXT SALARY'), ('date', 'SPECIFIC DATE')
)

GENDER = (
    ('male', 'MALE'), ('female', 'FEMALE')
)


RELIGION = (
    ('christianity', 'CHRISTIANITY'), ('islam', 'ISLAM'), ('others', 'OTHERS')
)

BLOOD_GROUP = (
        ('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'),
        ('o-', 'O-'),
)

GENOTYPE = (
        ('aa', 'AA'), ('as', 'AS'), ('ac', 'AC'), ('ss', 'SS')
)

MARITAL_STATUS = (
        ('single', 'SINGLE'), ('married', 'MARRIED'), ('widowed', 'WIDOWED'), ('divorced', 'DIVORCED')
)

INSURANCE_PROVIDER = (
        ('nhis', 'NHIS'),
)

CERTIFICATE_TYPE = (
        ('school leaving', 'SCHOOL LEAVING'), ('ond', 'OND'), ('hnd', 'HND')
)

WARD_TYPE = (
    ('general', 'GENERAL'), ('special', 'SPECIAL'), ('icu', 'INTENSIVE CARE UNIT'), ('isolation', 'ISOLATION')
)

CONSULTATION_PAYMENT_DURATION = (
    ('daily', 'DAILY'), ('weekly', 'WEEKLY'), ('monthly', 'MONTHLY'), ('annually', 'ANNUALLY')
)


PAYMENT_STATUS = (
    ('not paid', 'NOT PAID'), ('paid', 'PAID')
    # always maintain the "not paid" status as the first item in the tuple
)

COLLECTION_STATUS = (
    ('not collected', 'NOT COLLECTED'), ('collected', 'COLLECTED')
    # always maintain the "not collected" status as the first item in the tuple
)

CONDUCTED_STATUS = (
    ('internal', 'INTERNAL'), ('external', 'EXTERNAL')
)

CONSULTATION_QUEUE_STATUS = (
    ('awaiting', 'AWAITING'), ('progress', 'PROGRESS'), ('paused', 'PAUSED'), ('complete', 'COMPLETE')
)

CONSULTATION_STATUS = (
    ('not posted', 'NOT POSTED'), ('posted', 'posted'), ('progress', 'PROGRESS'), ('complete', 'COMPLETE')
)

CONSULTATION_STAGE = (
    ('new', 'NEW'), ('follow up', 'FOLLOW UP'), ('conclusion', 'CONCLUSION')
)


BANKS = (
    ('access bank', 'ACCESS BANK'), ('first bank', 'FIRST BANK'), ('uba', 'UNITED BANKS FOR AFRICA')
)

RECEIPT_FORMAT = (
    ('portrait', 'PORTRAIT'), ('landscape', 'LANDSCAPE')
)

ACTIVE_STATUS = (
    ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
)

LEAVE_CATEGORY = (
    ('maternity leave', 'MATERNITY LEAVE'), ('sick leave', 'SICK LEAVE'), ('others', 'OTHERS')
)

DURATION_TYPE = (
    ('day', 'DAY'), ('week', 'WEEK'), ('month', 'MONTH'), ('year', 'YEAR')
)

LEAVE_STATUS = (
    ('pending', 'PENDING'), ('approved', 'APPROVED'), ('declined', 'DECLINED')
)

ASSET_TYPE = (
        ('fixed', 'FIXED'), ('movable', 'MOVABLE')
)

DRUG_FORM = (
    ('capsule', 'CAPSULE'), ('injection', 'INJECTION'), ('syrup', 'SYRUP'), ('balm', 'BALM')
)
