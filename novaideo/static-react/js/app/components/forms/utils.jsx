import React from 'react';
import Checkbox from 'material-ui/Checkbox';
import Icon from 'material-ui/Icon';
import classNames from 'classnames';
import Tooltip from 'material-ui/Tooltip';

import TextBoxField from './widgets/TextBoxField';
import FilesPicker from './widgets/FilesPicker';
import Select from './widgets/Select';

export const renderTextBoxField = ({ input: { name, value, onChange }, placeholder, onCtrlEnter, autoFocus, style }) => {
  return (
    <TextBoxField
      autoFocus={autoFocus}
      style={style}
      onCtrlEnter={onCtrlEnter}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
    />
  );
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

export const renderFilesListField = ({ input: { value, onChange }, node, initRef }) => {
  return (
    <FilesPicker initRef={initRef} className="files-dropzone-list" value={value} onChange={onChange} multiple clickable>
      {node}
    </FilesPicker>
  );
};

export const renderSelect = ({ input: { value, onChange }, options, label, canAdd, initRef }) => {
  return <Select initRef={initRef} label={label} options={options} value={value} onChange={onChange} canAdd={canAdd} />;
};