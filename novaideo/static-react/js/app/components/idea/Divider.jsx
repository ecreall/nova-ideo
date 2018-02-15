/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import { blue } from 'material-ui/colors';

import { getFormattedDate } from '../../utils/globalFunctions';
import Divider from '../common/Divider';

const styles = {
  messageFixed: {
    borderRadius: 5,
    color: 'white',
    top: '70px !important',
    backgroundColor: blue[500]
  },
  message: {
    color: blue[500],
    backgroundColor: 'transparent'
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
    const createdAtF = getFormattedDate(node.createdAt, 'date.format', { today: 'date.today', yesterday: 'date.yesterday' });
    const dateSeparator = addDateSeparator && createdAtF;
    return (
      <Divider
        fullScreen
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