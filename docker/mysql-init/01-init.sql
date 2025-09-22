CREATE DATABASE IF NOT EXISTS `benchmark_fastapi` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `benchmark_django` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `benchmark_django_asgi` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `benchmark_fast_django_asgi` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'benchmark_user'@'%' IDENTIFIED BY 'benchmark_pass';
GRANT ALL PRIVILEGES ON `benchmark_fastapi`.* TO 'benchmark_user'@'%';
GRANT ALL PRIVILEGES ON `benchmark_django`.* TO 'benchmark_user'@'%';
GRANT ALL PRIVILEGES ON `benchmark_django_asgi`.* TO 'benchmark_user'@'%';
GRANT ALL PRIVILEGES ON `benchmark_fast_django_asgi`.* TO 'benchmark_user'@'%';
FLUSH PRIVILEGES;


