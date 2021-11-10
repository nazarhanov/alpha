# Database: Alpha

Clothing store

## Tables:

1. [Categories](#categories)
2. [Tags](#tags)
3. [Groups](#groups)
4. [SingleFields](#singlefields)
5. [MultiFields](#multifields)
6. [Products](#products)
7. [Sizes](#sizes)
8. [Colors](#colors)
9. [Images](#images)
10. [Reviews](#reviews)
11. [ProductsCategories](#productscategories)
12. [ProductsTags](#productstags)
13. [ProductsSizes](#productssizes)
14. [ProductsColors](#productscolors)

## ER Diagram

![Clothing store database diagram](./diagram.svg)

## Content:

### `Categories`

| name         | type         | note               |
| ------------ | ------------ | ------------------ |
| category_id  | INT          | PK, AUTO_INCREMENT |
| name         | VARCHAR(255) |                    |
| created_date | TIMESTAMP    |                    |
| updated_date | TIMESTAMP    |                    |
| parent_id    | INT          | FK to Categories   |

### `Tags`

| name         | type         | note               |
| ------------ | ------------ | ------------------ |
| tag_id       | INT          | PK, AUTO_INCREMENT |
| name         | VARCHAR(255) |                    |
| created_date | TIMESTAMP    |                    |
| updated_date | TIMESTAMP    |                    |

### `Groups`

| name         | type         | note               |
| ------------ | ------------ | ------------------ |
| group_id     | INT          | PK, AUTO_INCREMENT |
| name         | VARCHAR(255) |                    |
| created_date | TIMESTAMP    |                    |
| updated_date | TIMESTAMP    |                    |

### `SingleFields`

| name            | type          | note               |
| --------------- | ------------- | ------------------ |
| singel_field_id | INT           | PK, AUTO_INCREMENT |
| name            | VARCHAR(255)  | UNIQUE             |
| key             | VARCHAR(255)  |                    |
| value           | VARCHAR(1023) |                    |
| created_date    | TIMESTAMP     |                    |
| updated_date    | TIMESTAMP     |                    |
| group_id        | INT           | FK to Groups       |

### `MultiFields`

| name           | type          | note               |
| -------------- | ------------- | ------------------ |
| multi_field_id | INT           | PK, AUTO_INCREMENT |
| name           | VARCHAR(255)  |                    |
| key            | VARCHAR(255)  |                    |
| value          | VARCHAR(1023) |                    |
| created_date   | TIMESTAMP     |                    |
| updated_date   | TIMESTAMP     |                    |
| group_id       | INT           | FK to Groups       |

### `Products`

| name         | type         | note               |
| ------------ | ------------ | ------------------ |
| product_id   | INT          | PK, AUTO_INCREMENT |
| name         | VARCHAR(255) |                    |
| short_desc   | VARCHAR(255) |                    |
| full_desc    | TEXT         |                    |
| price        | DECIMAL      |                    |
| views        | INT UNSIGNED |                    |
| created_date | TIMESTAMP    |                    |
| updated_date | TIMESTAMP    |                    |

### `Sizes`

| name         | type         | note               |
| ------------ | ------------ | ------------------ |
| size_id      | INT          | PK, AUTO_INCREMENT |
| name         | VARCHAR(255) |                    |
| created_date | TIMESTAMP    |                    |
| updated_date | TIMESTAMP    |                    |

### `Colors`

| name         | type         | note               |
| ------------ | ------------ | ------------------ |
| color_id     | INT          | PK, AUTO_INCREMENT |
| name         | VARCHAR(255) |                    |
| value        | VARCHAR(255) |                    |
| created_date | TIMESTAMP    |                    |
| updated_date | TIMESTAMP    |                    |

### `Images`

| name         | type          | note               |
| ------------ | ------------- | ------------------ |
| image_id     | INT           | PK, AUTO_INCREMENT |
| source       | VARCHAR(2047) |                    |
| created_date | TIMESTAMP     |                    |
| updated_date | TIMESTAMP     |                    |
| product_id   | INT           | FK to Products     |
| color_id     | INT           | FK to Colors       |

### `Reviews`

| name         | type             | note               |
| ------------ | ---------------- | ------------------ |
| review_id    | INT              | PK, AUTO_INCREMENT |
| author       | VARCHAR(255)     |                    |
| content      | VARCHAR(1023)    |                    |
| photo        | VARCHAR(2047)    |                    |
| email        | VARCHAR(319)     |                    |
| rating       | TINYINT UNSIGNED |                    |
| created_date | TIMESTAMP        |                    |
| updated_date | TIMESTAMP        |                    |
| product_id   | INT              | FK to Products     |

### `ProductsCategories`

| name                | type      | note               |
| ------------------- | --------- | ------------------ |
| product_category_id | INT       | PK, AUTO_INCREMENT |
| created_date        | TIMESTAMP |                    |
| updated_date        | TIMESTAMP |                    |
| product_id          | INT       | FK to Products     |
| category_id         | INT       | FK to Categories   |

### `ProductsTags`

| name           | type      | note               |
| -------------- | --------- | ------------------ |
| product_tag_id | INT       | PK, AUTO_INCREMENT |
| created_date   | TIMESTAMP |                    |
| updated_date   | TIMESTAMP |                    |
| product_id     | INT       | FK to Products     |
| tag_id         | INT       | FK to Tags         |

### `ProductsSizes`

| name            | type      | note               |
| --------------- | --------- | ------------------ |
| product_size_id | INT       | PK, AUTO_INCREMENT |
| created_date    | TIMESTAMP |                    |
| updated_date    | TIMESTAMP |                    |
| product_id      | INT       | FK to Products     |
| size_id         | INT       | FK to Sizes        |

### `ProductsColors`

| name             | type      | note               |
| ---------------- | --------- | ------------------ |
| product_color_id | INT       | PK, AUTO_INCREMENT |
| created_date     | TIMESTAMP |                    |
| updated_date     | TIMESTAMP |                    |
| product_id       | INT       | FK to Products     |
| color_id         | INT       | FK to Colors       |
