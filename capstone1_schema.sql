DROP DATABASE IF EXISTS breed_picker;
CREATE DATABASE breed_picker;

\c breed_picker;

------------------------------------------------------------------------------------------------
-- TABLES:
------------------------------------------------------------------------------------------------

CREATE TABLE breeds
(
    id SERIAL PRIMARY KEY,
    name TEXT,
);


CREATE TABLE users
(
    id SERIAL PRIMARY KEY, 
    username TEXT,
    email TEXT,
    family_members_adults INTEGER,
    family_members_kids INTEGER,
    other_pets TEXT, --> dogs, cats, fish, reptiles, amphibians, small mammals (gerbil, hamster, guinea pig)
    environment TEXT,   --> urban (no yard), suburban(back yard), rural(multiple acres)  
    experience_level INTEGER   --> none (has never owned a dog), 
);  



CREATE TABLE characteristics 
(
    id SERIAL PRIMARY KEY,
    title TEXT, -->  (max_height_male, max_height_female, min_height_male,min_height_female, max_weight_male, max_weight_female, min_weight_male, min_weight_female, coat_length, shedding, drooling, exercise, barking, good_with_children, good_with_dogs, good_with_strangers)
)

CREATE TABLE reviews 
(
    id SERIAL PRIMARY KEY REFERENCES reviews,
    maintenance_rating INTEGER,
    behavior_rating INTEGER,
    intelligence_rating INTEGER,
    comments TEXT,
    breed_id INTEGER REFERENCES breeds, --> FOREIGN KEY, many-to-many
    user_id INTEGER REFERENCES users  --> FOREIGN KEY, one-to-many
);


CREATE TABLE dogs_in_home
(
    id SERIAL PRIMARY KEY,
    photo TEXT,
    breed_id INTEGER REFERENCES breeds, --> FOREIGN KEY, many-to-many
    user_id INTEGER REFERENCES users --> FOREIGN KEY, one-to-many
)


CREATE TABLE breeds_considering
(
    id SERIAL PRIMARY KEY,
    breed_id INTEGER REFERENCES breeds, --> FOREIGN KEY, many-to-many
    user_id INTEGER REFERENCES users, --> FOREIGN KEY, one-to-many
)


CREATE TABLE breed_charateristics
(
    id SERIAL PRIMARY KEY,
    value_rating INTEGER,  --> (scale of 1-5, 1 being least, 5 being most)
    breed_id INTEGER REFERENCES breeds, --> FOREIGN KEY, many-to-many
    characteristic_id INTEGER REFERENCES characteristics --> FOREIGN KEY, many-to-many
)


CREATE TABLE users_valued_characteristics
(
    id SERIAL PRIMARY KEY,
    value_rating INTEGER  --> (scale of 1-5, 1 being least, 5 being most)
    user_id INTEGER REFERENCES users, --> FOREIGN KEY, many-to-many
    characteristic_id INTEGER REFERENCES characteristics --> FOREIGN KEY, many-to-many
)


