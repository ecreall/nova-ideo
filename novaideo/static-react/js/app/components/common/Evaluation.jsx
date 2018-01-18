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
    textShadow: '0 0px 2px gray',
    fontSize: 25
  },
  tokenBottom: {
    color: '#ef6e18',
    textShadow: '0 0px 2px gray',
    fontSize: 25
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
    marginBottom: -15
  },
  tokenNbTop: {
    color: '#4eaf4e',
    fontSize: 13,
    fontWeight: 'bold',
    marginTop: -10
  },
  inactive: { color: '#c3c3c3', margin: 0 }
};

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
      <Icon style={{ ...styles.tokenTop, ...styles.inactive }} className={icon.top} />
      <span style={{ ...styles.tokenNbTop, ...styles.inactive }}>
        {text.top}
      </span>
      <span style={{ ...styles.tokenNbBottom, ...styles.inactive }}>
        {text.down}
      </span>
      <Icon style={{ ...styles.tokenBottom, ...styles.inactive }} className={icon.down} />
    </div>
  );
};

export default Evaluation;