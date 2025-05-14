import os
import platformdirs

save_dir = os.environ.get('WORKING_DIR') or platformdirs.user_data_dir('zen-explorer')
