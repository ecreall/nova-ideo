import React from 'react';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import { Picker } from 'emoji-mart';
import IconButton from 'material-ui/IconButton';
import InsertEmoticonIcon from 'material-ui-icons/InsertEmoticon';

const styles = {
  picker: {
    boxShadow: '0 5px 10px rgba(0,0,0,.12)',
    fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif',
    position: 'absolute',
    right: -35,
    bottom: 36,
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
      width: 41
    },
    buttonActive: {
      color: theme.palette.primary[500]
    },
    icon: {}
  };
};

class EmojiPicker extends React.Component {
  static defaultProps = {
    style: {}
  };

  constructor(props) {
    super(props);
    this.state = {
      opened: false
    };
    this.picker = null;
    this.button = null;
  }

  componentDidMount() {
    document.addEventListener('click', this.closePicker);
  }

  componentWillUnmount() {
    document.removeEventListener('click', this.closePicker);
  }

  openPicker = () => {
    this.setState({ opened: true });
  };

  closePicker = (event) => {
    if (this.state.opened && this.picker && !this.picker.contains(event.target)) {
      this.setState({ opened: false });
    }
  };

  onEmojiSelect = (emoji) => {
    const { onSelect } = this.props;
    if (onSelect) {
      this.setState({ opened: false });
      onSelect(emoji.colons);
    }
  };

  render() {
    const { theme, classes, style } = this.props;
    return (
      <div
        ref={(picker) => {
          this.picker = picker;
        }}
      >
        <IconButton
          className={classNames(classes.button, {
            [classes.buttonActive]: this.state.opened
          })}
          onClick={this.openPicker}
        >
          <InsertEmoticonIcon className={classes.icon} />
        </IconButton>

        {this.state.opened &&
          <Picker
            color={theme.palette.primary[500]}
            title="Emoji"
            emoji="slightly_smiling_face"
            sheetSize={32}
            style={{ ...styles.picker, ...style.picker }}
            onClick={this.onEmojiSelect}
          />}
      </div>
    );
  }
}

export default withStyles(classesStyles, { withTheme: true })(EmojiPicker);