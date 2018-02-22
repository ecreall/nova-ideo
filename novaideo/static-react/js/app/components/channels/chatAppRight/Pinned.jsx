/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';

import DetailsSection from './DetailsSection';
import { iconAdapter } from '../../../utils/globalFunctions';
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
      marginTop: -3,
      fontSize: '24px !important',
      color: theme.palette.danger[500]
    },
    sectionIconActive: {
      '&:hover': {
        color: theme.palette.danger[500]
      }
    }
  };
};

class Pinned extends React.Component {
  render() {
    const { id, channel, classes, totalCount, onOpen, open } = this.props;
    return (
      <DetailsSection
        id={id}
        classes={{
          sectionIcon: classes.sectionIcon,
          sectionIconActive: classes.sectionIconActive
        }}
        onOpen={onOpen}
        open={open}
        title={
          <span>
            <span>
              {I18n.t('channels.pinnedBlockTitle')}
            </span>
            <span className={classes.counter}>
              {totalCount && `(${totalCount})`}
            </span>
          </span>
        }
        Icon={iconAdapter('mdi-set mdi-pin')}
      >
        {open &&
          <Comments
            rightDisabled
            customScrollbar
            dynamicDivider={false}
            displayForm={false}
            channelId={channel.id}
            filter={{ pinned: true }}
            classes={{ container: classes.container, list: classes.container }}
          />}
      </DetailsSection>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Pinned);