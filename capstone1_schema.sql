DROP DATABASE IF EXISTS breed_picker;
CREATE DATABASE breed_picker;

\c breed_picker;

CREATE TABLE breeds
(
    id INTEGER PRIMARY KEY,
    name TEXT,
    max_height_male INTEGER,
    max_height_female INTEGER,
    min_height_male INTEGER,
    min_height_female INTEGER,
    max_weight_male INTEGER,
    max_weight_female INTEGER,
    min_weight_male INTEGER,
    min_weight_female INTEGER,
    coat_length INTEGER,
    shedding INTEGER,
    drooling INTEGER,
    exercise INTEGER, 
    barking INTEGER,
    good_with_children INTEGER,
    good_with_dogs INTEGER,
    good_with_strangers INTEGER,
    user_id INTEGER REFERENCES users,
    review_id INTEGER REFERENCES reviews
);

CREATE TABLE users
(
    id INTEGER PRIMARY KEY, 
    username TEXT,
    email TEXT,
    family_members_adults INTEGER,
    family_members_kids INTEGER,
    other_pets TEXT,
    environment TEXT,
    experience_level INTEGER,
    important_characteristics TEXT,
    dog_photo TEXT,
    breeds_considering_id INTEGER REFERENCES breeds,
    breeds_in_home_id INTEGER REFERENCES breeds,
    review_id INTEGER REFERENCES reviews
);  

CREATE TABLE reviews 
(
    id INTEGER PRIMARY KEY REFERENCES reviews,
    maintenance_rating INTEGER,
    behavior_rating INTEGER,
    intelligence_rating INTEGER,
    comments TEXT,
    breed_id INTEGER REFERENCES breeds,
    user_id INTEGER REFERENCES users
);


-- QUESTIONS FOR SONIA:
-- 1.   Would it be better to have a separate table called "favorites" or "my_breeds" for the fields of
--      breeds_considering_id, breeds_in_home_id, instead of keeping them in the users table?  I like the simplicity 
--      of fewer tables, but I'm not sure it will be any easier to deal with in practice than 
--      having a fourth table.  