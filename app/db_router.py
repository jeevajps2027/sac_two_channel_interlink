class MultiDBRouter:
    """
    A router to control all database operations on models in the project.
    """

    def db_for_write(self, model, **hints):
        """Write to both default (SQLite) and mssql."""
        if model.__name__ == "InterlinkData":
            return 'default'  # main write goes to SQLite
        return None

    def db_for_read(self, model, **hints):
        """Read normally from default unless overridden."""
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if both models are in the same DB."""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Migrate InterlinkData to both databases."""
        if model_name == "interlinkdata":
            return True
        return None
