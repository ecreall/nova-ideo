import glamorous from 'glamorous';
import Button from 'material-ui/Button';
import IconButtonBase from 'material-ui/IconButton';

const StyledButton = glamorous(Button)((props) => {
  const background = props.background || '#2ea664';
  return {
    background: background,
    color: props.color || '#fff',
    lineHeight: '19px',
    fontWeight: 700,
    textDecoration: 'none',
    cursor: 'pointer',
    textShadow: '0 1px 1px rgba(0,0,0,.2)',
    border: 'none',
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
      backgroundColor: background,
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