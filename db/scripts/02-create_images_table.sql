USE `LabelImgWeb`;

CREATE TABLE `images` (
	`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`filename` VARCHAR(100) COLLATE 'utf8_general_ci' NOT NULL,
	`updated_at` DATETIME NOT NULL,
	`created_at` DATETIME NOT NULL,
	`removed_at` DATETIME,
    KEY `filename_index` (`filename`)
) ENGINE='InnoDB' COLLATE 'utf8_general_ci';