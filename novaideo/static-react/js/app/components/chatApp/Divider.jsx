/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import { Translate } from 'react-redux-i18n';
import { connect } from 'react-redux';

import { getFormattedDate } from '../../utils/globalFunctions';
import Divider from '../common/Divider';
import { STYLE_CONST } from '../../constants';

export class DumbCommentDivider extends React.Component {
  addDateSeparator = () => {
    const { node, reverted } = this.props;
    const item = reverted ? this.props.next : this.props.previous;
    if (!item) return true;
    return !Moment(node.createdAt).isSame(Moment(item.createdAt), 'day');
  };

  addUnread = () => {
    const { node, reverted, dividerProps } = this.props;
    const item = reverted ? this.props.next : this.props.previous;
    const unreadComments = dividerProps.unreadCommentsIds;
    const isUnread = unreadComments.includes(node.id);
    if (!item) return isUnread;
    const nextIsUnread = unreadComments.includes(item.id);
    return isUnread && !nextIsUnread;
  };

  render() {
    const {
      node,
      index,
      eventId,
      drawer,
      reverted,
      dividerProps: { fullScreen, ignorDrawer, dynamic, unreadCommentsIds }
    } = this.props;
    const addUnread = this.addUnread();
    const addDateSeparator = this.addDateSeparator();
    const createdAtF = getFormattedDate(node.createdAt, 'date.format', { today: 'date.today', yesterday: 'date.yesterday' });
    const dateSeparator = addDateSeparator && createdAtF;
    let dividerShift = 0;
    if (!ignorDrawer) {
      dividerShift = drawer ? STYLE_CONST.drawerWidth : 0;
    }
    return dateSeparator || addUnread ? (
      <Divider
        dynamic={dynamic}
        fullScreen={fullScreen}
        reverted={reverted}
        index={index}
        alert={addUnread}
        message={dateSeparator}
        alertMessage={<Translate value="channels.unreadMessages" count={unreadCommentsIds.length} />}
        eventId={eventId}
        shift={dividerShift}
        fixedTop={65}
      />
    ) : null;
  }
}

export const mapStateToProps = (state) => {
  return {
    drawer: state.apps.drawer.open
  };
};

export default connect(mapStateToProps)(DumbCommentDivider);