USE `LabelImgWeb`;

CREATE TABLE `boundingboxes` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `image_id` int NOT NULL,
  `class_name` varchar(50) COLLATE 'utf8_general_ci' NOT NULL,
  `top` int NOT NULL,
  `left` int NOT NULL,
  `width` int NOT NULL,
  `height` int NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  FOREIGN KEY (`image_id`) REFERENCES `images` (`id`)
) ENGINE='InnoDB' COLLATE 'utf8_general_ci';