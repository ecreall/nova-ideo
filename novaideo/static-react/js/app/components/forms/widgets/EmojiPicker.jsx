import React from 'react';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import { Picker } from 'emoji-mart';
import IconButton from '@material-ui/core/IconButton';
import InsertEmoticonIcon from '@material-ui/icons/InsertEmoticon';

import { Menu } from '../../common/menu';
import { PICKER_EMOJI_SHEET_APPLE_32 } from '../../../constants';

const styles = {
  picker: {
    fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif',
    position: 'relative',
    zIndex: 2
  }
};

const classesStyles = (theme) => {
  return {
    button: {
      display: 'flex',
      color: 'gray',
      cursor: 'pointer',
      height: 41,
      width: 35
    },
    buttonActive: {
      color: theme.palette.primary[500]
    },
    icon: {},
    menuPaper: {
      width: 'auto',
      maxHeight: 'inherit',
      overflowX: 'auto',
      borderRadius: 6,
      '& > ul': {
        padding: 0
      }
    }
  };
};

class EmojiPicker extends React.Component {
  static defaultProps = {
    style: {}
  };

  state = {
    opened: false
  };

  picker = null;

  openPicker = () => {
    this.setState({ opened: true });
  };

  closePicker = () => {
    this.setState({ opened: false });
  };

  onEmojiSelect = (emoji) => {
    const { onSelect } = this.props;
    if (onSelect) {
      onSelect(emoji.colons);
    }
    this.setState({ opened: false });
    if (this.picker) this.picker.close();
  };

  render() {
    const { theme, classes, style } = this.props;
    return (
      <Menu
        id="emoji-picker"
        initRef={(picker) => {
          this.picker = picker;
        }}
        classes={{
          menuPaper: classes.menuPaper
        }}
        onOpen={this.openPicker}
        onClose={this.closePicker}
        activator={
          <IconButton
            className={classNames(classes.button, {
              [classes.buttonActive]: this.state.opened
            })}
          >
            <InsertEmoticonIcon className={classes.icon} />
          </IconButton>
        }
      >
        <Picker
          color={theme.palette.primary[500]}
          title="Emoji"
          emoji="slightly_smiling_face"
          sheetSize={32}
          style={{ ...styles.picker, ...style.picker }}
          onClick={this.onEmojiSelect}
          backgroundImageFn={() => {
            return PICKER_EMOJI_SHEET_APPLE_32;
          }}
        />
      </Menu>
    );
  }
}

export default withStyles(classesStyles, { withTheme: true })(EmojiPicker);