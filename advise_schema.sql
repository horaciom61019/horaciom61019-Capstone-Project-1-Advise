CREATE TABLE "User"(
    "id" INTEGER NOT NULL,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "advice" TEXT NOT NULL;
);
ALTER TABLE
    "User" ADD PRIMARY KEY("id");
CREATE TABLE "Advice"(
    "id" INTEGER NOT NULL,
    "advice" TEXT NOT NULL,
    "user_id" INTEGER NOT NULL
);
ALTER TABLE
    "advice" ADD PRIMARY KEY("id");
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
    "advice_id" INTEGER NOT NULL
);
ALTER TABLE
    "Likes" ADD PRIMARY KEY("id");
ALTER TABLE
    "advice" ADD CONSTRAINT "advice_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "Likes"("id");