import os
from dotenv import dotenv_values
from src.utils import init_logger

init_logger()
# Custom config
cscf = dotenv_values()
# Loading config from env
DATA_DIR = os.getenv('DATA_DIR', cscf.get('DATA_DIR', '/data'))

# QC MYSQL
MYSQL_HOST = os.getenv('MYSQL_HOST', cscf.get('MYSQL_HOST'))
MYSQL_PORT = int(os.getenv('MYSQL_PORT', cscf.get('MYSQL_PORT', 3306)))
MYSQL_DB = os.getenv('MYSQL_DB', cscf.get('MYSQL_DB'))
MYSQL_USER = os.getenv('MYSQL_USER', cscf.get('MYSQL_USER'))
MYSQL_PASS = os.getenv('MYSQL_PASS', cscf.get('MYSQL_PASS'))

# CH Labs
CH_HOST = os.getenv('CH_HOST', cscf.get('CH_HOST', ''))
CH_PORT = int(os.getenv('CH_PORT', cscf.get('CH_PORT', 8123)))
CH_USER = os.getenv('CH_USER', cscf.get('CH_USER', ''))
CH_PASS = os.getenv('CH_PASS', cscf.get('CH_PASS', ''))

# Redis
REDIS_USER = os.getenv("REDIS_USER", cscf.get("REDIS_USER", ""))
REDIS_HOST = os.getenv('REDIS_HOST', cscf.get('REDIS_HOST', ''))
REDIS_PASS = os.getenv('REDIS_PASS', cscf.get('REDIS_PASS', ''))
REDIS_PORT = 6379

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', cscf.get('OPENAI_API_KEY', ''))
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', cscf.get('DEEPSEEK_API_KEY', ''))
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', cscf.get('DEEPSEEK_BASE_URL', ''))

USER_MOOD_ACTIONS = ['view_mood', 'like_mood', 'save_mood', 'apply_mood', 'report_mood']
MOOD_ACTION_WEIGHTS = {
    'view_mood': 1,
    'view_post_outside': 1,
    'view_post_detail': 1,
    'like_mood': 2,
    'like_post': 2,
    'save_mood': 3,
    'apply_mood': 4,
    'report_mood': -1
}
USER_POST_ACTIONS = ['view_post_outside', 'view_post_detail', 'like_post', 'comment_post', 'create_post', 'report_post',
                     'repost_post']

CATEGORY_DIMS = ['Relaxation', 'Focus', 'Motivation', 'Playfulness', 'Euphoria', 'Calm Confidence',
                 'Sensory Enhancement', 'Inspiration']
NUMBER_OF_CATEGORIES = len(CATEGORY_DIMS)
EMBEDDING_DIMS = 384

# define file name
USER_PROFILE_FN = 'user_profiles.gz'
USER_EMBEDDING_FN = 'user_embeddings.gz'
USER_PROFILE_CLUSTER_FN = 'user_profiles_cluster.gz'

POST_EMBEDDING_FN = 'post_embeddings.gz'

MOOD_INFORMATION_FN = 'mood_information.gz'
MOOD_EMBEDDING_FN = 'mood_embeddings.gz'
MOOD_EMBEDDING_INDEX_FN = 'mood_embeddings_index.usearch'
MOOD_PROFILE_FN = 'mood_profiles.gz'
MOOD_PROFILE_INDEX_FN = 'mood_profiles_index.usearch'

KAFKA_HOST = os.getenv('KAFKA_HOST', cscf.get('KAFKA_HOST', ''))
KAFKA_PORT = int(os.getenv('KAFKA_PORT', cscf.get('KAFKA_PORT', 9093)))
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', cscf.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9093'))

KAFKA_MOOD_EMBEDDING_TYPE = "recommendator.mood_service.st_embedding"
KAFKA_USER_SECTION_TYPE = "recommendator.user_service.sections.mood"

MOOD_KAFKA_TOPIC = os.getenv('MOOD_KAFKA_TOPIC', cscf.get('MOOD_KAFKA_TOPIC', 'mood-recommendator-embedding'))

DB_TIMEZONE = 'UTC'
