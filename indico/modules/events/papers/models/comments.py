# This file is part of Indico.
# Copyright (C) 2002 - 2016 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from indico.core.db import db
from indico.core.db.sqlalchemy.review_comments import ReviewCommentMixin
from indico.util.locators import locator_property
from indico.util.string import format_repr, return_ascii, text_to_repr


class PaperReviewComment(ReviewCommentMixin, db.Model):
    __tablename__ = 'review_comments'
    __table_args__ = {'schema': 'event_paper_reviewing'}
    user_backref_name = 'review_comments'
    user_modified_backref_name = 'modified_review_comments'

    @declared_attr
    def revision_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey('event_paper_reviewing.revisions.id'),
            index=True,
            nullable=False
        )

    @declared_attr
    def paper_revision(cls):
        return db.relationship(
            'PaperRevision',
            lazy=True,
            backref=db.backref(
                'comments',
                primaryjoin='(PaperReviewComment.revision_id == PaperRevision.id) & ~PaperReviewComment.is_deleted',
                order_by=cls.created_dt,
                cascade='all, delete-orphan',
                lazy=True,
            )
        )

    @locator_property
    def locator(self):
        return dict(self.paper_revision.locator, comment_id=self.id)

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'id', 'revision_id', is_deleted=False, _text=text_to_repr(self.text))

    def can_edit(self, user):
        if user is None:
            return False
        elif self.user == user:
            return True
        elif self.revision.contribution.event_new.can_manage(user, role='paper_manager'):
            return True
        else:
            return False