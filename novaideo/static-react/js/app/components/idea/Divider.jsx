/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import { blue } from 'material-ui/colors';
import { I18n } from 'react-redux-i18n';

import Divider from '../common/Divider';

const styles = {
  messageFixed: {
    borderRadius: 5,
    color: 'white',
    top: '70px !important',
    backgroundColor: blue[500]
  },
  message: {
    color: blue[500]
  },
  divider: {
    margin: 0
  }
};

class IdeasDivider extends React.Component {
  addDateSeparator = () => {
    const { node, previous } = this.props;
    if (!previous) return true;
    return !Moment(node.createdAt).isSame(Moment(previous.createdAt), 'day');
  };

  render() {
    const { node, index, eventId } = this.props;
    const addDateSeparator = this.addDateSeparator();
    const today = Moment();
    const isToday = today.isSame(Moment(node.createdAt), 'day');
    const yesterday = today.subtract(1, 'days').startOf('day');
    const isYesterday = yesterday.isSame(Moment(node.createdAt), 'day');
    const format = (isToday && 'date.today') || (isYesterday && 'date.yesterday');
    const dateSeparator = addDateSeparator && (format ? I18n.t(format) : Moment(node.createdAt).format(I18n.t('date.format')));
    return (
      <Divider
        isGlobal
        index={index}
        message={dateSeparator}
        eventId={eventId}
        shift={0}
        fixedTop={65}
        style={{
          divider: styles.divider,
          message: styles.message,
          messageFixed: styles.messageFixed
        }}
      />
    );
  }
}

export default IdeasDivider;