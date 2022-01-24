-- Add permissions to 'indoc_vre' DB for notification and unsubscribe

INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'notification', 'view', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'notification', 'create', 'p')
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'notification', 'update', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'notification', 'delete', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('admin', '*', 'notification', 'view', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('contributor', '*', 'notification', 'view', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('collaborator', '*', 'notification', 'view', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('member', '*', 'notification', 'view', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('visitor', '*', 'notification', 'view', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'email', 'create', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'unsubscribe', 'create', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('admin', '*', 'unsubscribe', 'create', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('contributor', '*', 'unsubscribe', 'create', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('collaborator', '*', 'unsubscribe', 'create', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('member', '*', 'unsubscribe', 'create', 'p');
INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('visitor', '*', 'unsubscribe', 'create', 'p');
