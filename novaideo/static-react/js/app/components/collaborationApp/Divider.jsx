/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import { withStyles } from 'material-ui/styles';

import { getFormattedDate } from '../../utils/globalFunctions';
import Divider from '../common/Divider';

const styles = (theme) => {
  return {
    messageFixed: {
      borderRadius: 5,
      color: 'white !important',
      backgroundColor: `${theme.palette.primary[500]} !important`
    },
    message: {
      color: theme.palette.primary[500],
      backgroundColor: 'transparent'
    },
    divider: {
      margin: 0
    }
  };
};

export class DumbIdeasDivider extends React.PureComponent {
  addDateSeparator = () => {
    const { node, previous } = this.props;
    if (!previous) return true;
    return !Moment(node.createdAt).isSame(Moment(previous.createdAt), 'day');
  };

  render() {
    const { node, index, eventId, classes } = this.props;
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
        classes={{
          divider: classes.divider,
          message: classes.message,
          messageFixed: classes.messageFixed
        }}
      />
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbIdeasDivider);