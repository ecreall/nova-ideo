import glamorous from 'glamorous';
import Button from 'material-ui/Button';
import IconButtonBase from 'material-ui/IconButton';

const StyledButton = glamorous(Button)((props) => {
  const background = props.background || '#2ea664';
  const color = props.color || '#fff';
  return {
    background: background,
    color: color,
    lineHeight: '19px',
    fontWeight: 700,
    textDecoration: 'none',
    cursor: 'pointer',
    textShadow: '0 1px 1px rgba(0,0,0,.2)',
    border: `solid 1px ${color}`,
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
      backgroundColor: color,
      color: background,
      border: `solid 1px ${background}`,
      boxShadow: '0 1px 2px 1px rgba(128, 128, 128, 0.4)'
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

export const IconButton = glamorous(IconButtonBase)((props) => {
  return props.textColor
    ? {
      color: props.textColor,
      '&:hover': {
        color: props.textColor
      }
    }
    : {};
});

export default StyledButton;