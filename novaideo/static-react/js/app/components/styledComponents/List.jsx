import glamorous from 'glamorous';
import MuiListItem from '@material-ui/core/ListItem';
import MuiListItemText from '@material-ui/core/ListItemText';
import MuiListItemIcon from '@material-ui/core/ListItemIcon';

export const ListItem = glamorous(MuiListItem)((props) => {
  return {
    borderRadius: 5,
    padding: '0 16px 0 8px',
    margin: '0 15px',
    width: '100%',
    minHeight: 28,
    transition: 'none',
    '&:hover, &:focus, &:active': {
      backgroundColor: props.hoverColor,
      '& .menu-item-icon': {
        color: 'white'
      },
      '& .menu-item-text': {
        color: 'white',
        textShadow: '0 1px 0 rgba(0,0,0,.1)'
      }
    }
  };
});

export const ListItemText = glamorous(MuiListItemText)((props) => {
  return {
    padding: 0,
    '& .menu-item-text': {
      flex: '1 1 auto',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      fontSize: 15,
      color: props.color || '#2c2d30'
    }
  };
});

export const ListItemIcon = glamorous(MuiListItemIcon)((props) => {
  return {
    width: 20,
    height: 28,
    marginRight: 10,
    color: props.iconColor || '#a0a0a2'
  };
});