import glamorous from 'glamorous';
import Button from '@material-ui/core/Button';
import IconButtonBase from '@material-ui/core/IconButton';

const StyledButton = glamorous(Button, { filterProps: ['background'] })(({ background, color }) => {
  const backgroundColor = background || '#2ea664';
  const textColor = color || '#fff';
  return {
    background: backgroundColor,
    color: textColor,
    lineHeight: '19px',
    fontWeight: 700,
    textDecoration: 'none',
    cursor: 'pointer',
    textShadow: '0 1px 1px rgba(0,0,0,.2)',
    border: `solid 1px ${textColor}`,
    borderRadius: 4,
    boxShadow: 'none',
    position: 'relative',
    display: 'inline-block',
    verticalAlign: 'bottom',
    textAlign: 'center',
    whiteSpace: 'nowrap',
    margin: 0,
    textTransform: 'none',
    '&:hover': {
      backgroundColor: textColor,
      color: backgroundColor,
      border: `solid 1px ${backgroundColor}`,
      boxShadow: '0 1px 2px 1px rgba(128, 128, 128, 0.4)'
    },
    '&:disabled': {
      backgroundColor: '#dadada'
    }
  };
});

export const CancelButton = glamorous(Button)(() => {
  return {
    background: '#f9f9f9',
    color: '#333',
    lineHeight: '19px',
    fontWeight: 700,
    textDecoration: 'none',
    cursor: 'pointer',
    textShadow: '0 1px 1px rgba(0,0,0,.2)',
    border: '1px solid #c7cacd',
    borderRadius: 4,
    boxShadow: 'none',
    position: 'relative',
    display: 'inline-block',
    verticalAlign: 'bottom',
    textAlign: 'center',
    whiteSpace: 'nowrap',
    margin: 0,
    textTransform: 'none'
  };
});

export const IconButton = glamorous(IconButtonBase, { filterProps: ['textColor'] })(({ textColor }) => {
  return textColor
    ? {
      color: textColor,
      '&:hover': {
        color: textColor
      }
    }
    : {};
});

export default StyledButton;