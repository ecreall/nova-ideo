import React from 'react';
import Icon from 'material-ui/Icon';

const styles = {
  containerStyle: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'flex-end'
  },
  styleText: {
    marginLeft: 4,
    fontSize: 17
  },
  styleIcon: {
    marginTop: 2,
    color: 'rgb(88, 88, 88)'
  }
};

const IconWithText = ({ name, text, containerStyle, styleText, styleIcon, iconSize, iconColor, numberOfLines }) => {
  return (
    <div style={containerStyle || styles.containerStyle}>
      <Icon style={styleIcon || styles.styleIcon} className={name} size={iconSize} color={iconColor} />
      <span style={styleText || styles.styleText} numberOfLines={numberOfLines}>
        {text}
      </span>
    </div>
  );
};

export default IconWithText;