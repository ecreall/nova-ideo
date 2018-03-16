/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';

import AllignedActions from '../common/AllignedActions';
import { ACTIONS } from '../../processes';
import { getActions } from '../../utils/processes';
import { getFormattedDate } from '../../utils/globalFunctions';
import UserAvatar from '../user/UserAvatar';
import UserTitle from '../user/UserTitle';
import IdeaMenu from './IdeaMenu';
import IdeaAppBarTitle from './IdeaAppBarTitle';

const styles = (theme) => {
  return {
    header: {
      display: 'flex',
      flexDirection: 'column',
      margin: '0 10px',
      position: 'relative'
    },
    headerTitle: {
      fontSize: 15,
      color: '#2c2d30',
      fontWeight: 900,
      lineHeight: 'normal'
    },
    titleContainer: {
      display: 'flex'
    },
    headerAddOn: {
      color: '#999999ff',
      fontSize: 12,
      lineHeight: 'normal'
    },
    actionsContainer: {
      height: 41,
      width: 'auto'
    },
    actionsText: {
      color: '#2c2d30',
      marginRight: 15,
      fontSize: 14,
      fontWeight: 400,
      width: 35,
      '&:hover': {
        color: theme.palette.info['700']
      }
    },
    actionsIcon: {
      fontWeight: 100,
      fontSize: '20px !important',
      marginRight: 5,
      marginTop: -2,
      height: 20,
      width: 20
    },

    appBarContainer: {
      display: 'flex',
      justifyContent: 'space-between'
    },

    appbarActions: {
      display: 'flex'
    },
    menu: {
      position: 'relative',
      border: 'none',
      boxShadow: 'none',
      marginRight: 5
    },
    menuButton: {
      color: '#2c2d30'
    }
  };
};

const IdeaAppBar = (props) => {
  const { idea, hasEvaluation, stats, processManager, classes } = props;
  const author = idea.author;
  const authorPicture = author && author.picture;
  const isAnonymous = author && author.isAnonymous;
  const createdAtF3 = getFormattedDate(idea.createdAt, 'date.format3');
  const communicationActions = getActions(idea.actions, { tags: ACTIONS.communication });
  return (
    <div className={classes.appBarContainer}>
      <div className={classes.titleContainer}>
        <UserAvatar isAnonymous={isAnonymous} picture={authorPicture} title={author.title} />
        <div className={classes.header}>
          <UserTitle node={author} classes={{ title: classes.headerTitle }} />
          <span className={classes.headerAddOn}>
            {createdAtF3}
          </span>
        </div>
      </div>
      <IdeaAppBarTitle idea={idea} hasEvaluation={hasEvaluation} stats={stats} />
      <div className={classes.appbarActions}>
        <AllignedActions
          actions={communicationActions}
          onActionClick={processManager.performAction}
          overlayPosition="bottom"
          classes={{
            actionsContainer: classes.actionsContainer,
            actionsText: classes.actionsText,
            actionsIcon: classes.actionsIcon
          }}
        />
        <IdeaMenu open idea={idea} classes={{ container: classes.menu, button: classes.menuButton }} />
      </div>
    </div>
  );
};

export default withStyles(styles, { withTheme: true })(IdeaAppBar);