from app.extensions import db


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    client = db.Column(db.String(5), nullable=False)
    product_area = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Feature %r>'.format(self.title)

    @staticmethod
    def reorder_priority(priority, client):
        priority_to_update = priority
        features_to_update_count = Feature.query.filter_by(client=client, priority=priority_to_update).count()
        while features_to_update_count > 1:
            feature_to_update = Feature.query.filter_by(client=client, priority=priority_to_update) \
                .order_by('id').first()
            feature_to_update.priority = feature_to_update.priority + 1
            priority_to_update = priority_to_update + 1
            features_to_update_count = Feature.query.filter_by(client=client, priority=priority_to_update) \
                .count()

