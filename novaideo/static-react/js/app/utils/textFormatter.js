const FORMAT = {
  block: {
    prefix: '&#x60;&#x60;&#x60;',
    suffix: '&#x60;&#x60;&#x60;',
    className: 'format-mrkdwn-pre',
    tag: 'pre'
  },
  code: {
    prefix: '&#x60;',
    suffix: '&#x60;',
    className: 'format-code-var',
    tag: 'code'
  },
  sitation: {
    prefix: '\\[\\[',
    suffix: '\\]\\]',
    className: 'format-blockquote',
    tag: 'div'
  },
  sitationDanger: {
    prefix: '\\[d\\[',
    suffix: '\\]d\\]',
    className: 'format-blockquote danger',
    tag: 'div'
  },
  sitationSuccess: {
    prefix: '\\[s\\[',
    suffix: '\\]s\\]',
    className: 'format-blockquote success',
    tag: 'div'
  },
  sitationWarning: {
    prefix: '\\[w\\[',
    suffix: '\\]w\\]',
    className: 'format-blockquote warning',
    tag: 'div'
  },
  sitationInfo: {
    prefix: '\\[i\\[',
    suffix: '\\]i\\]',
    className: 'format-blockquote info',
    tag: 'div'
  },
  bold: {
    prefix: '\\*\\*\\*',
    suffix: '\\*\\*\\*',
    className: 'format-text-bold',
    tag: 'span'
  },
  italic: {
    prefix: '\\*i\\*',
    suffix: '\\*i\\*',
    className: 'format-text-italic',
    tag: 'span'
  },
  underline: {
    prefix: '\\*u\\*',
    suffix: '\\*u\\*',
    className: 'format-text-underline',
    tag: 'span'
  }
};

const regexWrapperText = (list, className, tag) => {
  if (list.length < 3) return list.join(' ');
  const first = list.shift() || '';
  const last = list.pop() || '';
  return `${first}<${tag} class="${className}">${regexWrapperText(list, className, tag)}</${tag}>${last}`;
};

export const formatText = (text) => {
  let result = text;
  Object.keys(FORMAT).forEach((key) => {
    const format = FORMAT[key];
    const regex = new RegExp(`${format.prefix}(.*?)${format.suffix}`);
    result = regexWrapperText(result.split(regex), format.className, format.tag);
  });

  return result;
};