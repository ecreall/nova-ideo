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
      height: 45,
      width: 'auto',
      paddingRight: 0
    },
    actionsText: {
      color: '#2c2d30',
      marginRight: 5,
      fontSize: 14,
      fontWeight: 400,
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
      justifyContent: 'space-between',
      alignItems: 'center'
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
    },
    menuAction: {
      borderRight: 'none'
    },
    publishAction: {
      marginRight: '20px !important',
      minWidth: 'auto',
      minHeight: 'auto',
      padding: '5px 10px'
    }
  };
};

const IdeaAppBar = (props) => {
  const { idea, hasEvaluation, stats, processManager, classes, theme } = props;
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
        <IdeaMenu
          open
          overlayPosition="bottom"
          idea={idea}
          onActionClick={processManager.performAction}
          classes={{ container: classes.menu, button: classes.menuButton, action: classes.menuAction }}
          actionsProps={{
            publish: { className: classes.publishAction, type: 'button', props: { background: theme.palette.success[500] } }
          }}
        />
      </div>
    </div>
  );
};

export default withStyles(styles, { withTheme: true })(IdeaAppBar);