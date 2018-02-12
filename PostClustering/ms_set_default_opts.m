function opts=ms_set_default_opts(opts,def_opts)
names=fieldnames(def_opts);
for ii=1:length(names)
    if (isstruct(def_opts.(names{ii})))
        if (~isfield(opts,names{ii}))
            opts.(names{ii})=struct;
        end;
        opts.(names{ii})=ms_set_default_opts(opts.(names{ii}),def_opts.(names{ii}));
    else
        if (~isfield(opts,names{ii}))
            opts.(names{ii})=def_opts.(names{ii});
        end;
    end;
end;
end