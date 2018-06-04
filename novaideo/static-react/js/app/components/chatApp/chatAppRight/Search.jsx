import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';

import Comments from '../Comments';

const styles = {
  commentsContainer: {
    height: '100% !important',
    margin: 0,
    width: 'calc(100% + 8px)'
  },
  list: {
    height: '100% !important'
  },
  noResult: {
    paddingLeft: 25,
    marginBottom: 15,
    fontSize: 15,
    color: '#717274',
    marginTop: 20,
    lineHeight: '20px'
  }
};

export const DumbSearch = ({ channel, searchProps, classes }) => {
  return (
    <Comments
      rightDisabled
      customScrollbar
      dynamicDivider={false}
      displayForm={false}
      displayFooter={false}
      NoItems={() => {
        return <div className={classes.noResult}>{I18n.t('channels.noResultBlock')}</div>;
      }}
      channelId={channel.id}
      filter={{ text: searchProps && searchProps.filter && searchProps.filter.text }}
      classes={{ container: classes.commentsContainer, list: classes.list }}
    />
  );
};

export const mapStateToProps = (state) => {
  return {
    searchProps: state.apps.chatApp.right.props
  };
};
export default withStyles(styles)(connect(mapStateToProps)(DumbSearch));