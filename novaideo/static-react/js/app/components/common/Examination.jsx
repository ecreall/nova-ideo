import React from 'react';
import FontIcon from 'material-ui/FontIcon';

const styles = {
  circleContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 5,
    paddingTop: 7,
    paddingBottom: 7,
    backgroundColor: '#e7e7e7',
    borderWidth: 0.5,
    borderColor: '#ddd',
    borderRadius: 3,
    elevation: 2,
    shadowColor: 'gray',
    shadowOpacity: 0.8,
    shadowRadius: 2,
    shadowOffset: {
      height: 1,
      width: 0
    },
    width: 25
  },
  circle: {
    color: 'gray',
    textShadowColor: 'gray',
    textShadowRadius: 4
  },
  circleTop: {
    color: '#f13b2d',
    textShadowColor: '#f13b2d',
    textShadowOffset: { width: 0.1, height: 0.1 }
  },
  circleMiddle: {
    color: '#ef6e18',
    textShadowColor: '#ef6e18',
    textShadowOffset: { width: 0.1, height: 0.1 }
  },
  circleBottom: {
    color: '#4eaf4e',
    textShadowColor: '#4eaf4e',
    textShadowOffset: { width: 0.1, height: 0.1 }
  }
};

const Examination = ({ value, message }) => {
  return (
    <div
      style={styles.circleContainer}
      onPress={() => {
        alert(message);
      }}
      hitSlop={{ top: 15, bottom: 15, left: 15, right: 15 }}
    >
      <div>
        <FontIcon
          style={[styles.circle, value === 'top' ? styles.circleTop : {}]}
          className="mdi-set mdi-checkbox-blank-circle"
          size={15}
        />
        <FontIcon
          style={[styles.circle, value === 'middle' ? styles.circleMiddle : {}]}
          className="mdi-set mdi-checkbox-blank-circle"
          size={15}
        />
        <FontIcon
          style={[styles.circle, value === 'bottom' ? styles.circleBottom : {}]}
          className="mdi-set mdi-checkbox-blank-circle"
          size={15}
        />
      </div>
    </div>
  );
};

export default Examination;