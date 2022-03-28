CREATE TABLE "User"(
    "id" INTEGER NOT NULL,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "advise" TEXT NOT NULL
);
ALTER TABLE
    "User" ADD PRIMARY KEY("id");
CREATE TABLE "Advise"(
    "id" INTEGER NOT NULL,
    "advise" TEXT NOT NULL,
    "user_id" INTEGER NOT NULL
);
ALTER TABLE
    "Advise" ADD PRIMARY KEY("id");
CREATE TABLE "Follows"(
    "id" INTEGER NOT NULL,
    "user_being_followed_id" INTEGER NOT NULL,
    "user_following_id" INTEGER NOT NULL
);
ALTER TABLE
    "Follows" ADD PRIMARY KEY("id");
CREATE TABLE "Likes"(
    "id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "advise_id" INTEGER NOT NULL
);
ALTER TABLE
    "Likes" ADD PRIMARY KEY("id");
ALTER TABLE
    "Advise" ADD CONSTRAINT "advise_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "Likes"("id");