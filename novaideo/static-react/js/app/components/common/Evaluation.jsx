import React from 'react';

import FontIcon from 'material-ui/FontIcon';

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
    textShadowRadius: 2
  },
  tokenBottom: {
    color: '#ef6e18',
    textShadowColor: 'gray',
    textShadowOffset: { width: -1, height: 1 },
    textShadowRadius: 2
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

const Evaluation = ({ icon, text, action, onPress, onLongPress, active }) => {
  if (active) {
    return (
      <div style={styles.tokenContainer}>
        <div
          onPress={() => {
            return onPress.top(action.top);
          }}
          onLongPress={() => {
            return onLongPress.top(action.top);
          }}
          hitSlop={{ top: 15, bottom: 15, left: 15, right: 15 }}
        >
          <FontIcon style={styles.tokenTop} className={icon.top} size={35} />
        </div>
        <span style={styles.tokenNbTop}>
          {text.top}
        </span>
        <span style={styles.tokenNbBottom}>
          {text.down}
        </span>
        <div
          onPress={() => {
            return onPress.down(action.down);
          }}
          onLongPress={() => {
            return onLongPress.down(action.down);
          }}
          hitSlop={{ top: 15, bottom: 15, left: 15, right: 15 }}
        >
          <FontIcon style={styles.tokenBottom} className={icon.down} size={35} />
        </div>
      </div>
    );
  }
  return (
    <div style={styles.tokenContainer}>
      <FontIcon style={[styles.tokenTop, { color: inactiveColor }]} className={icon.top} size={30} />
      <span style={[styles.tokenNbTop, { color: inactiveColor }]}>
        {text.top}
      </span>
      <span style={[styles.tokenNbBottom, { color: inactiveColor }]}>
        {text.down}
      </span>
      <FontIcon style={[styles.tokenBottom, { color: inactiveColor }]} className={icon.down} size={30} />
    </div>
  );
};

export default Evaluation;