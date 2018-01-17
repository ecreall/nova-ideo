import React from 'react';
import Icon from 'material-ui/Icon';

const styles = {
  containerStyle: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'flex-end'
  },
  styleText: {
    fontSize: 17,
    color: 'rgb(88, 88, 88)'
  },
  styleIcon: {
    fontSize: 17,
    color: 'rgb(88, 88, 88)'
  }
};

const IconWithText = ({ name, text, containerStyle, styleText, styleIcon }) => {
  return (
    <div style={{ ...styles.containerStyle, ...containerStyle }}>
      <Icon style={{ ...styles.styleIcon, ...styleIcon }} className={name} />
      <span style={{ ...styles.styleText, ...styleText }}>
        {text}
      </span>
    </div>
  );
};

export default IconWithText;