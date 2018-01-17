import React from 'react';
import Checkbox from 'material-ui/Checkbox';
import Icon from 'material-ui/Icon';
import classNames from 'classnames';
import Tooltip from 'material-ui/Tooltip';

import TextBoxField from './widgets/TextBoxField';
import FilesPicker from './widgets/FilesPicker';
import Select from './widgets/Select';

export const renderTextBoxField = ({ input: { name, value, onChange }, placeholder, onCtrlEnter }) => {
  return <TextBoxField onCtrlEnter={onCtrlEnter} name={name} placeholder={placeholder} value={value} onChange={onChange} />;
};

export const renderAnonymousCheckboxField = ({ input: { value, onChange }, label, classes }) => {
  const anonymous = Boolean(value);
  return (
    <Tooltip title={anonymous ? 'Disable anonymity' : 'Remain anonymous'} placement="top">
      <Checkbox
        icon={<Icon className={classNames(classes.maskIcon, 'mdi-set mdi-guy-fawkes-mask')} />}
        checkedIcon={<Icon className={classNames(classes.maskIcon, 'mdi-set mdi-guy-fawkes-mask')} />}
        label={label}
        value={value}
        onChange={onChange}
        classes={{
          default: classes.maskDefault,
          checked: classes.maskChecked
        }}
      />
    </Tooltip>
  );
};

export class RenderFilesListField extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.picker = null;
  }

  render() {
    const { input: { value, onChange }, node } = this.props;
    return (
      <FilesPicker
        ref={(picker) => {
          this.picker = picker;
        }}
        className="files-dropzone-list"
        value={value}
        onChange={onChange}
        multiple
        clickable
      >
        {node}
      </FilesPicker>
    );
  }
}

export const renderSelect = ({ input: { name, value, onChange }, options, label, canAdd }) => {
  return <Select label={label} options={options} value={value} onChange={onChange} />;
};