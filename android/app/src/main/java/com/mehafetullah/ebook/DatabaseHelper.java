package com.mehafetullah.ebook;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHelper extends SQLiteOpenHelper {
    public static final String DATABASE_NAME = "mehafetullah.db";
    public static final int DATABASE_VERSION = 1;

    public static final String TABLE_PAGES = "pages";
    public static final String COLUMN_PAGE_NUM = "page_num";
    public static final String COLUMN_TITLE = "title";
    public static final String COLUMN_CONTENT_HTML = "content_html";
    public static final String COLUMN_RAW_TEXT = "raw_text";

    private static final String TABLE_CREATE =
            "CREATE TABLE " + TABLE_PAGES + " (" +
                    COLUMN_PAGE_NUM + " INTEGER PRIMARY KEY, " +
                    COLUMN_TITLE + " TEXT, " +
                    COLUMN_CONTENT_HTML + " TEXT, " +
                    COLUMN_RAW_TEXT + " TEXT" +
                    ");";

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(TABLE_CREATE);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_PAGES);
        onCreate(db);
    }
}
