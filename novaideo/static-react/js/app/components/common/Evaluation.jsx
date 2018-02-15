import React from 'react';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';

import Tooltip from './overlay/Tooltip';
import OverlayTrigger from './overlay/OverlayTrigger';

const styles = {
  tokenContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 5,
    paddingBottom: 5,
    marginBottom: 10
  },
  tokenTop: {
    color: '#4eaf4e',
    textShadow: '0 0px 2px rgba(128, 128, 128, 0.4)',
    fontSize: 25,
    transition: 'all .1s ease-in-out',
    display: 'block',
    '&:hover': {
      fontSize: 30
    }
  },
  tokenBottom: {
    color: '#ef6e18',
    textShadow: '0 0px 2px rgba(128, 128, 128, 0.4)',
    fontSize: 25,
    transition: 'all .1s ease-in-out',
    display: 'block',
    '&:hover': {
      fontSize: 30
    }
  },
  buttonTop: {
    color: '#4eaf4e',
    display: 'block'
  },
  buttonBottom: {
    color: '#ef6e18',
    display: 'block'
  },
  tokenNbBottom: {
    color: '#ef6e18',
    fontSize: 13,
    fontWeight: 'bold',
    marginBottom: -8,
    height: 13,
    lineHeight: 'normal'
  },
  tokenNbTop: {
    color: '#4eaf4e',
    fontSize: 13,
    fontWeight: 'bold',
    marginTop: -12,
    height: 13,
    lineHeight: 'normal'
  },
  inactive: {
    color: '#c3c3c3',
    fontSize: '25px !important',
    '&:hover': {
      fontSize: 25
    }
  },
  nbInactive: {
    color: '#c3c3c3',
    margin: 0
  },
  buttonTopOverlay: {
    position: 'absolute',
    '& .tooltip-inner': {
      backgroundColor: '#4eaf4e'
    }
  },
  buttonBottomOverlay: {
    position: 'absolute',
    '& .tooltip-inner': {
      backgroundColor: '#ef6e18'
    }
  },
  itemContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 5,
    height: 53
  },
  inactiveItemContainer: {
    height: 40
  }
};

const Evaluation = ({ icon, text, actions, onClick, active, classes }) => {
  if (active) {
    return (
      <div className={classes.tokenContainer}>
        <div className={classes.itemContainer}>
          <IconButton
            className={classes.buttonTop}
            onClick={() => {
              return onClick.top(actions.top);
            }}
          >
            <OverlayTrigger
              overlay={
                <Tooltip className={classes.buttonTopOverlay}>
                  {I18n.t(actions.top.description)}
                </Tooltip>
              }
              placement="right"
            >
              <Icon className={classNames(classes.tokenTop, icon.top)} />
            </OverlayTrigger>
          </IconButton>
          <div className={classes.tokenNbTop}>
            {text.top}
          </div>
        </div>
        <div className={classes.itemContainer}>
          <div className={classes.tokenNbBottom}>
            {text.down}
          </div>
          <IconButton
            className={classes.buttonBottom}
            onClick={() => {
              return onClick.down(actions.down);
            }}
          >
            <OverlayTrigger
              overlay={
                <Tooltip className={classes.buttonBottomOverlay}>
                  {I18n.t(actions.down.description)}
                </Tooltip>
              }
              placement="right"
            >
              <Icon className={classNames(classes.tokenBottom, icon.down)} />
            </OverlayTrigger>
          </IconButton>
        </div>
      </div>
    );
  }
  return (
    <div className={classes.tokenContainer}>
      <div className={classNames(classes.itemContainer, classes.inactiveItemContainer)}>
        <Icon className={classNames(classes.tokenTop, classes.inactive, icon.top)} />
        <div className={classNames(classes.tokenNbTop, classes.nbInactive)}>
          {text.top}
        </div>
      </div>
      <div className={classNames(classes.itemContainer, classes.inactiveItemContainer)}>
        <div className={classNames(classes.tokenNbBottom, classes.nbInactive)}>
          {text.down}
        </div>
        <Icon className={classNames(classes.tokenBottom, classes.inactive, icon.down)} />
      </div>
    </div>
  );
};

export default withStyles(styles)(Evaluation);