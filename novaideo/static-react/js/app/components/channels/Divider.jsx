/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';

import Divider from '../common/Divider';

export class DumbCommentDivider extends React.Component {
  addDateSeparator = () => {
    const { node, next } = this.props;
    if (!next) return true;
    const createdAt = Moment(node.createdAt).format('D-M-YYYY');
    const nextCreatedAt = Moment(next.createdAt).format('D-M-YYYY');
    return nextCreatedAt !== createdAt;
  };

  addUnread = () => {
    const { node, next, itemdata } = this.props;
    if (!next) return false;
    const unreadComments = itemdata.unreadCommentsIds;
    const isUnread = unreadComments.includes(node.id);
    const nextIsUnread = unreadComments.includes(next.id);
    return isUnread && !nextIsUnread;
  };

  render() {
    const { node, index, channelsDrawer } = this.props;
    const addUnread = this.addUnread();
    const addDateSeparator = this.addDateSeparator();
    const isToday = Moment().diff(Moment(node.createdAt), 'days') === 0;
    const dateSeparator =
      addDateSeparator && (isToday ? I18n.t('date.today') : Moment(node.createdAt).format(I18n.t('date.format')));
    return dateSeparator || addUnread
      ? <Divider
        index={index}
        alert={addUnread}
        message={dateSeparator}
        alertMessage="Unread"
        eventId="comments-scroll"
        shift={channelsDrawer ? 220 : 0}
        fixedTop={65}
      />
      : null;
  }
}

export const mapStateToProps = (state) => {
  return {
    channelsDrawer: state.apps.chatApp.drawer
  };
};

export default connect(mapStateToProps)(DumbCommentDivider);