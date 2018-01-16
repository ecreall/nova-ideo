import React from 'react';
import Icon from 'material-ui/Icon';

const styles = {
  circleContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgb(231, 231, 231)',
    border: 'solid 1px rgba(167, 167, 167, 0.22)',
    borderRadius: 3,
    width: 25,
    boxShadow: '0 1px 2px rgba(128, 128, 128, 0.6)'
  },
  circle: {
    color: 'gray'
  },
  circleTop: {
    color: '#f13b2d',
    textShadow: '0 0px 4px #f13b2d'
  },
  circleMiddle: {
    color: '#ef6e18',
    textShadow: '0 0px 4px #ef6e18'
  },
  circleBottom: {
    color: '#4eaf4e',
    textShadow: '0 0px 4px #4eaf4e'
  }
};

const Examination = ({ value, message }) => {
  return (
    <div
      style={styles.circleContainer}
      onClick={() => {
        alert(message);
      }}
    >
      <Icon
        style={Object.assign({}, styles.circle, value === 'top' ? styles.circleTop : {})}
        className="mdi-set mdi-checkbox-blank-circle"
        size={15}
      />
      <Icon
        style={Object.assign({}, styles.circle, value === 'middle' ? styles.circleMiddle : {})}
        className="mdi-set mdi-checkbox-blank-circle"
        size={15}
      />
      <Icon
        style={Object.assign({}, styles.circle, value === 'bottom' ? styles.circleBottom : {})}
        className="mdi-set mdi-checkbox-blank-circle"
        size={15}
      />
    </div>
  );
};

export default Examination;