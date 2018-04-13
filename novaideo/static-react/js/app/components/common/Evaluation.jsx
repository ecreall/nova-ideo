import React from 'react';
import IconButton from 'material-ui/IconButton';
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
  tokenContainerBig: {
    marginBottom: 25
  },
  token: {
    textShadow: '0 0px 2px rgba(128, 128, 128, 0.4)',
    fontSize: '25px !important',
    transition: 'all .1s ease-in-out',
    display: 'block',
    '&:hover': {
      fontSize: '30px !important'
    }
  },
  tokenBig: {
    fontSize: '35px !important',
    display: 'block',
    '&:hover': {
      fontSize: '40px !important'
    }
  },
  tokenTop: {
    color: '#4eaf4e'
  },
  tokenBottom: {
    color: '#ef6e18'
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
  tokenNbBottomBig: {
    fontSize: 14,
    marginBottom: -5
  },
  tokenNbTop: {
    color: '#4eaf4e',
    fontSize: 13,
    fontWeight: 'bold',
    marginTop: -12,
    height: 13,
    lineHeight: 'normal'
  },
  tokenNbTopBig: {
    fontSize: 14,
    marginTop: -3
  },
  inactive: {
    color: '#c3c3c3',
    fontSize: '25px !important',
    '&:hover': {
      fontSize: 25
    }
  },
  inactiveBig: {
    color: '#c3c3c3',
    fontSize: '35px !important',
    '&:hover': {
      fontSize: '35px !important'
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
  itemContainerBig: {
    marginTop: 15
  },
  inactiveItemContainer: {
    height: 40
  }
};

export const DumbEvaluation = ({ icon, text, actions, onClick, active, big, classes }) => {
  const IconTop = icon.top;
  const IconDown = icon.down;
  if (active) {
    return (
      <div className={classNames(classes.tokenContainer, { [classes.tokenContainerBig]: big })}>
        <div className={classNames(classes.itemContainer, { [classes.itemContainerBig]: big })}>
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
              <IconTop className={classNames(classes.token, classes.tokenTop, { [classes.tokenBig]: big })} />
            </OverlayTrigger>
          </IconButton>
          <div className={classNames(classes.tokenNbTop, { [classes.tokenNbTopBig]: big })}>
            {text.top}
          </div>
        </div>
        <div className={classNames(classes.itemContainer, { [classes.itemContainerBig]: big })}>
          <div className={classNames(classes.tokenNbBottom, { [classes.tokenNbBottomBig]: big })}>
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
              <IconDown className={classNames(classes.token, classes.tokenBottom, { [classes.tokenBig]: big })} />
            </OverlayTrigger>
          </IconButton>
        </div>
      </div>
    );
  }
  return (
    <div className={classNames(classes.tokenContainer, { [classes.tokenContainerBig]: big })}>
      <div className={classNames(classes.itemContainer, classes.inactiveItemContainer, { [classes.itemContainerBig]: big })}>
        <IconTop
          className={classNames(classes.token, classes.tokenTop, classes.inactive, {
            [classes.tokenBig]: big,
            [classes.inactiveBig]: big
          })}
        />
        <div className={classNames(classes.tokenNbTop, classes.nbInactive, { [classes.tokenNbBottomBig]: big })}>
          {text.top}
        </div>
      </div>
      <div className={classNames(classes.itemContainer, classes.inactiveItemContainer, { [classes.itemContainerBig]: big })}>
        <div className={classNames(classes.tokenNbBottom, classes.nbInactive, { [classes.tokenNbBottomBig]: big })}>
          {text.down}
        </div>
        <IconDown
          className={classNames(classes.token, classes.tokenBottom, classes.inactive, {
            [classes.tokenBig]: big,
            [classes.inactiveBig]: big
          })}
        />
      </div>
    </div>
  );
};

export default withStyles(styles)(DumbEvaluation);