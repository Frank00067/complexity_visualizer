class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"), nullable=False)
    algorithm = db.Column(db.String(100))
    result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    image = db.relationship("Image", backref="analyses")
