/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';

import Comments from '../Comments';

const styles = {
  container: {
    borderTop: '1px solid #e8e8e8'
  },
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

class Search extends React.Component {
  render() {
    const { channel, searchProps, classes } = this.props;
    return (
      <div className={classes.container}>
        <Comments
          rightDisabled
          customScrollbar
          dynamicDivider={false}
          displayForm={false}
          displayFooter={false}
          NoItems={() => {
            return (
              <div className={classes.noResult}>
                {I18n.t('channels.noResultBlock')}
              </div>
            );
          }}
          channelId={channel.id}
          filter={{ text: searchProps && searchProps.filter && searchProps.filter.text }}
          classes={{ container: classes.commentsContainer, list: classes.list }}
        />
      </div>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    searchProps: state.apps.chatApp.right.props
  };
};
export default withStyles(styles)(connect(mapStateToProps)(Search));