# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI — https://github.com/BharatChandra-sys/fake-news-extension
from database import engine
import sqlalchemy as sa

with engine.begin() as conn:
    conn.execute(sa.text("ALTER TABLE users ADD COLUMN IF NOT EXISTS tier VARCHAR DEFAULT 'free'"))
    print("Tier column added successfully")
