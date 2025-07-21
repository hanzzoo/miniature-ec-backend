ALTER USER 'user'@'%' IDENTIFIED WITH mysql_native_password BY 'user_password';
FLUSH PRIVILEGES;

SET NAMES 'utf8mb4';

CREATE TABLE IF NOT EXISTS products (
  product_id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255),
  category_id VARCHAR(255),
  price VARCHAR(255),
  description VARCHAR(255),
  specs VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


INSERT INTO products (product_id, name, category_id, price, description, specs) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'Fender Stratocaster', 'guitar', 128000, '伝統的なシングルコイル搭載モデル。多様な音作りに対応。', 'ボディ: アルダー, ピックアップ: シングルx3, 色: サンバースト'),
('550e8400-e29b-41d4-a716-446655440001', 'Gibson Les Paul Standard', 'guitar', 198000, '太く力強い音が特徴の王道レスポールモデル。', 'ボディ: マホガニー, ピックアップ: ハムバッカーx2, 色: チェリーサンバースト'),

('550e8400-e29b-41d4-a716-446655440002', 'BOSS DS-1 Distortion', 'effector', 7000, '定番のディストーション。歪み初心者にもおすすめ。', 'タイプ: ディストーション, 電源: 9V, カラー: オレンジ'),
('550e8400-e29b-41d4-a716-446655440003', 'Electro-Harmonix Big Muff Pi', 'effector', 11000, '伝説的なサスティンとファズサウンド。', 'タイプ: ファズ, 電源: 9V, 製造: USA'),

('550e8400-e29b-41d4-a716-446655440004', 'Elixir Nanoweb 10-46', 'string', 1600, '長寿命コーティング弦。明るくバランスの良い音色。', 'ゲージ: 10-46, 素材: ニッケル, 対応: エレキギター'),
('550e8400-e29b-41d4-a716-446655440005', 'D’Addario EXL110', 'string', 1200, '多くのプレイヤーに愛されるスタンダード弦。', 'ゲージ: 10-46, 素材: ニッケル, 対応: エレキギター');


CREATE TABLE IF NOT EXISTS cart (
  instance VARCHAR(255) PRIMARY KEY,
  user_id VARCHAR(255),
  created_at VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS cartItem (
  instance VARCHAR(255),
  product_id VARCHAR(255),
  quantity INT,
  added_at VARCHAR(255),
  PRIMARY KEY (instance, product_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS user (
  user_id VARCHAR(255) PRIMARY KEY,
  user_name VARCHAR(255),
  user_email VARCHAR(255),
  user_password VARCHAR(255),
  created_at VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS purchase (
  purchase_id VARCHAR(255) PRIMARY KEY,
  user_id VARCHAR(255),
  purchased_at VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;