/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';
import InsertDriveFileIcon from 'material-ui-icons/InsertDriveFile';

import DetailsSection from './DetailsSection';
import Comments from '../Comments';

const styles = (theme) => {
  return {
    container: {
      height: '100% !important'
    },
    list: {
      height: '100%'
    },
    counter: {
      fontFamily: 'LatoWebLight',
      fontWeight: 100,
      marginLeft: 5,
      fontSize: 14
    },
    sectionIcon: {
      color: theme.palette.warning[500]
    },
    sectionIconActive: {
      '&:hover': {
        color: theme.palette.warning[500]
      }
    },
    listItem: {
      borderBottom: '1px solid #e8e8e8'
    },
    listItemActive: {
      borderBottom: 'none'
    }
  };
};

class Files extends React.Component {
  render() {
    const { id, channel, classes, totalCount, onOpen, open } = this.props;
    return (
      <DetailsSection
        id={id}
        classes={{
          sectionIcon: classes.sectionIcon,
          sectionIconActive: classes.sectionIconActive,
          listItem: classes.listItem,
          listItemActive: classes.listItemActive
        }}
        onOpen={onOpen}
        open={open}
        title={
          <span>
            <span>
              {I18n.t('channels.filesBlockTitle')}
            </span>
            <span className={classes.counter}>
              {totalCount && `(${totalCount})`}
            </span>
          </span>
        }
        Icon={InsertDriveFileIcon}
      >
        {open &&
          <Comments
            rightDisabled
            customScrollbar
            dynamicDivider={false}
            displayForm={false}
            channelId={channel.id}
            filter={{ file: true }}
            classes={{ container: classes.container, list: classes.container }}
          />}
      </DetailsSection>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Files);