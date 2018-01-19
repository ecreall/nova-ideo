import React from 'react';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';

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
    '&:hover': {
      fontSize: 30
    }
  },
  tokenBottom: {
    color: '#ef6e18',
    textShadow: '0 0px 2px rgba(128, 128, 128, 0.4)',
    fontSize: 25,
    transition: 'all .1s ease-in-out',
    '&:hover': {
      fontSize: 30
    }
  },
  buttonTop: {
    color: '#4eaf4e'
  },
  buttonBottom: {
    color: '#ef6e18'
  },
  tokenNbBottom: {
    color: '#ef6e18',
    fontSize: 13,
    fontWeight: 'bold',
    marginBottom: -13,
    height: 17
  },
  tokenNbTop: {
    color: '#4eaf4e',
    fontSize: 13,
    fontWeight: 'bold',
    marginTop: -13,
    height: 17
  },
  inactive: {
    color: '#c3c3c3',
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
  }
};

const Evaluation = ({ icon, text, actions, onClick, active, classes }) => {
  if (active) {
    return (
      <div className={classes.tokenContainer}>
        <IconButton
          className={classes.buttonTop}
          onClick={() => {
            return onClick.top(actions.top);
          }}
        >
          <OverlayTrigger
            overlay={
              <Tooltip className={classes.buttonTopOverlay}>
                {actions.top.description}
              </Tooltip>
            }
            placement="right"
          >
            <Icon className={classNames(classes.tokenTop, icon.top)} size={35} />
          </OverlayTrigger>
        </IconButton>
        <span className={classes.tokenNbTop}>
          {text.top}
        </span>
        <span className={classes.tokenNbBottom}>
          {text.down}
        </span>
        <IconButton
          className={classes.buttonBottom}
          onClick={() => {
            return onClick.down(actions.down);
          }}
        >
          <OverlayTrigger
            overlay={
              <Tooltip className={classes.buttonBottomOverlay}>
                {actions.down.description}
              </Tooltip>
            }
            placement="right"
          >
            <Icon className={classNames(classes.tokenBottom, icon.down)} />
          </OverlayTrigger>
        </IconButton>
      </div>
    );
  }
  return (
    <div className={classes.tokenContainer}>
      <Icon className={classNames(classes.tokenTop, classes.inactive, icon.top)} />
      <span className={classNames(classes.tokenNbTop, classes.nbInactive)}>
        {text.top}
      </span>
      <span className={classNames(classes.tokenNbBottom, classes.nbInactive)}>
        {text.down}
      </span>
      <Icon className={classNames(classes.tokenBottom, classes.inactive, icon.down)} />
    </div>
  );
};

export default withStyles(styles)(Evaluation);