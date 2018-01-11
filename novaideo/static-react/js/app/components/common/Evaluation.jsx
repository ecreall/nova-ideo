import React from 'react';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';

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
    textShadowColor: 'gray',
    textShadowOffset: { width: -1, height: 1 },
    textShadowRadius: 2,
    fontSize: 30
  },
  tokenBottom: {
    color: '#ef6e18',
    textShadowColor: 'gray',
    textShadowOffset: { width: -1, height: 1 },
    textShadowRadius: 2,
    fontSize: 30
  },
  buttonTop: {
    color: '#4eaf4e'
  },
  buttonBottom: {
    color: '#ef6e18'
  },
  tokenNbBottom: {
    color: '#ef6e18',
    fontWeight: 'bold'
  },
  tokenNbTop: {
    color: '#4eaf4e',
    fontWeight: 'bold'
  }
};

const inactiveColor = '#a9a9a9';

const Evaluation = ({ icon, text, action, onPress, active }) => {
  if (active) {
    return (
      <div style={styles.tokenContainer}>
        <IconButton
          style={styles.buttonTop}
          onClick={() => {
            return onPress.top(action.top);
          }}
        >
          <Icon style={styles.tokenTop} className={icon.top} size={35} />
        </IconButton>
        <span style={styles.tokenNbTop}>
          {text.top}
        </span>
        <span style={styles.tokenNbBottom}>
          {text.down}
        </span>
        <IconButton
          style={styles.buttonBottom}
          onClick={() => {
            return onPress.down(action.down);
          }}
        >
          <Icon style={styles.tokenBottom} className={icon.down} />
        </IconButton>
      </div>
    );
  }
  return (
    <div style={styles.tokenContainer}>
      <Icon style={Object.assign({}, styles.tokenTop, { color: inactiveColor })} className={icon.top} />
      <span style={Object.assign({}, styles.tokenNbTop, { color: inactiveColor })}>
        {text.top}
      </span>
      <span style={Object.assign({}, styles.tokenNbBottom, { color: inactiveColor })}>
        {text.down}
      </span>
      <Icon style={Object.assign({}, styles.tokenBottom, { color: inactiveColor })} className={icon.down} />
    </div>
  );
};

export default Evaluation;