# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10325  GET              /                                                dashboard
 12380  GET              /api/abo/status                                  api_abo_status
 12334  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11113  GET              /api/automation/status                           api_automation_status
 11135  POST             /api/automation/toggle                           api_automation_toggle
 20141  GET              /api/channel/categories                          api_channel_categories
 20147  POST             /api/channel/set                                 api_channel_set
 19994  GET              /api/channels/status                             api_channels_status
 19668  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19651  GET              /api/clips                                       api_clips
 19697  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19569  GET              /api/debug/threads                               api_debug_threads
 12345  GET              /api/events                                      api_events
 11824  GET              /api/events/stream                               api_events_stream
 11651  GET              /api/health                                      api_health
 19610  POST             /api/highlights/config                           api_highlights_config
 10255  POST             /api/login                                       dashboard_login_submit
 12670  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11739  GET              /api/notify/status                               api_notify_status
 11750  POST             /api/notify/test                                 api_notify_test
 12434  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12411  GET              /api/proxy/trend                                 api_proxy_trend
 19717  GET              /api/tts/<fn>                                    api_tts_file
 20494  GET              /api/upload_window                               api_upload_window
 11941  GET              /archive/<int:eid>/download                      archive_download
 11969  GET              /download/<int:recording_id>                     download
 11898  GET              /health                                          health
 19478  GET              /healthz                                         healthz
 10246  GET              /login                                           dashboard_login_page
 10280  GET              /logout                                          dashboard_logout
 10287  GET              /manifest.webmanifest                            pwa_manifest
 20467  GET              /overlay                                         overlay_page
 10311  GET              /pwa-icon-<variant>.png                          pwa_icon
 10297  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   202  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   222  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   249  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   509  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   526  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   578  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   600  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   539  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   565  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   239  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   460  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   489  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   409  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   422  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   518  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   395  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   270  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   315  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   339  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   326  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   166  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   284  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   136  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   376  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   431  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (66)

```
  2171  /about                  Ueber diesen Bot
   890  /ai                     
  2171  /aireset                KI-Kontext zuruecksetzen
  1302  /ask                    
   991  /assign_role            
  1041  /ban                    
  2126  /botstats               
  2171  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2171  /bulkadd                Mehrere User auf einmal tracken · a b c
  2171  /cleanup                Alte Aufnahmen aufraeumen
  1557  /clearwarns             
  2090  /clip                   
  2075  /clipoftheweek          
  1428  /clips                  
  2171  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   946  /create_category        
   917  /create_channel         
   981  /create_group           
   956  /create_role            
   932  /create_voice           
  1180  /daily                  
  2171  /diag                   Vollstaendige Diagnose
  2171  /einnahmen              Einnahmen und Spenden
  1331  /event                  
  1373  /events                 
  1467  /follow                 
  1456  /help                   
  1031  /kick                   
  1155  /leaderboard            
  2171  /live                   Live-Status sofort pruefen · @user
  1415  /livenow                
  2171  /logs                   Letzte Fehler aus dem Log
  2171  /pause                  Tracking pausieren · @user
  1443  /post_test              
  1263  /profile                
  1063  /purge                  
  2171  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2171  /quota                  Speicher-Quota
  1142  /rank                   
  1403  /recstatus              
  1001  /remove_role            
  2171  /report                 Azrael-Sentinel-Wochenreport
   903  /restream_status        
  2171  /resume                 Tracking fortsetzen · @user
  1011  /set_channel_perms      
  1106  /setup_community        
  1123  /setup_targets          
  1499  /stats                  
   862  /status                 
  2171  /stoprec                Laufende Aufnahme sauber beenden · @user
  1595  /streaminfo             
  2171  /summary                Tageszusammenfassung
  2171  /sysres                 System-Ressourcen
  2171  /teststream             Recorder-Selbsttest · @user
  2171  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1051  /timeout                
  1567  /topstreamers           
  2171  /topusers               Top-Streamer nach Aufnahmen
   792  /track                  
  2171  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   875  /tracklist              
  1481  /unfollow               
  2171  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   824  /untrack                
  1520  /warn                   
  1543  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2329  on_member_join
  2291  on_message
  2192  on_raw_reaction_add
  2364  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-476    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (51 Funktionen)

```
   489-494    _alle_getrackten
  1672-1723   _award_xp
  1894-1923   _clip_week_leader
  1947-1961   _clipoftheweek_loop
  2481-2543   _community_events_loop
  1629-1651   _dc_client
  1654-1663   _dc_offen
  2583-2618   _disc_automod_check
   404-409    _disc_sprache_setzen
  1726-1774   _discord_ai_automod
   613-652    _discord_automod
  1777-1797   _discord_azrael_reply
  1964-2440   _discord_run_once
   239-297    _discord_start
   300-354    _ensure_discord_invite
  2446-2478   _ensure_error_channel
   425-438    _ensure_rank_roles
   755-769    _ensure_team_roles
  2546-2576   _error_channel_loop
   662-666    _guard
   582-610    _handle_voice_ai
   412-422    _is_admin
  1842-1853   _liveboard_loop
   669-687    _on_level_up
   578-579    _par_chat_id
  1926-1944   _post_clip_of_week
  1856-1874   _post_weekly_digest
   441-467    _provision_base_channels
   470-486    _provision_user_channels
  1395-1488   _reg_betrieb
  1077-1169   _reg_community_setup
  1172-1252   _reg_daily_profil
  1295-1392   _reg_frage_events
   849-905    _reg_info
  1023-1074   _reg_moderation
  1255-1292   _reg_profil
   972-1020   _reg_rollen
   908-969    _reg_server
  1491-1578   _reg_streamer
  1581-1626   _reg_system
   783-846    _reg_tracking
   722-752    _run_tg_handler
   565-575    _tracked_usernames
   156-218    _uebernehmen
  1806-1839   _update_liveboard
  1877-1891   _weekly_digest_loop
   497-502    _ziel_guild
   505-536    _ziele_abgleichen
   545-562    _ziele_sync_loop
   539-542    _ziele_takt_min
   221-224    starte
```

## Top-Level-Symbole in bot.py (553 Funktionen, 3 Klassen)

```
 25396-25418  _abbruch_datenbank_unlesbar
  2666-2667   _abo_key
  2687-2705   _abo_probe_dump
 25514-25530  _abschied_wachen
 25533-25551  _abschluss
 16237-16244  _ad_allowlist
 17239-17245  _agent_for
 17248-17264  _ai_telemetry
 17761-17779  _alert
 21362-21412  _alert_monitor_loop
 21794-21856  _announce_loop
  3562-3572   _anthropic_key
  3579-3581   _anthropic_model
  9910-9913   _arg_int
  2658-2663   _as_dict
 25094-25103  _async_exc_handler
 17942-17964  _audio_tap_cmd
 18644-18703  _audio_tap_melden
 17978-18002  _audio_tap_sammler
  9259-9292   _aufnahme_beim_stopp_sichern
 18366-18379  _aufnahme_chat_beginnen
 18413-18463  _aufnahme_chat_einarbeiten
 18361-18363  _aufnahme_chat_modus
 24343-24345  _aufnahme_deckel
 18382-18394  _aufnahme_fertigmachen
  9295-9313   _aufnahme_platz_frei
 25478-25498  _aufnahmen_abschliessen
 25421-25475  _aufraeumen
 10109-10178  _auth_cookie
 10067-10105  _auth_guard
  1907-1912   _auto_on
 19330-19348  _auto_restream_loop
 13914-13956  _avatar_frames_laden
 22877-22892  _azrael_broadcast_reply
 22777-22799  _azrael_chat_reply
 22749-22774  _azrael_chat_should_reply
 22805-22807  _azrael_gate_cfg
 17269-17283  _azrael_live_state
 20380-20394  _azrael_overlay_state
 17643-17697  _azrael_proactive_loop
 17087-17143  _azrael_reaction_to_chats
 22810-22817  _azrael_reply_all_chats
 22736-22746  _azrael_self_names
 22845-22874  _azrael_send_to
 13875-13911  _azrael_spricht
 14218-14231  _azrael_stimme_stumm
 17289-17310  _azrael_system
 21496-21499  _backup_active
 21577-21590  _backup_loop
 24432-24436  _betrieb
 25167-25176  _brain_crowdsec_snap
 25323-25326  _brain_db_health
 21283-21292  _brain_growth_loop
 10504-10531  _brain_growth_snapshot
  2591-2611   _brain_hint_delay
 25239-25274  _brain_moderation_snap
  6508-6536   _brain_notify
 25329-25351  _brain_recording_snap
 25179-25236  _brain_restream_health
 25354-25367  _brain_tiktok_status_snap
 11803-11820  _browser_push
  6548-6635   _build_daily_summary
 14265-14269  _build_restream_cmd
  5261-5288   _can_stop_tracking
  2020-2042   _capture_set_cookies
 12488-12491  _cfg_get
 12494-12496  _cfg_set
 20102-20137  _channel_set_all
 13071-13074  _chat_connected
 13077-13093  _chat_disconnected
  8888-8899   _chat_is_forum
 18330-18355  _chat_listener_abbauen
 13113-13115  _chat_sanitize
 13056-13068  _chat_stat
 13096-13099  _chat_stats_snapshot
  3880-3892   _check_ai_models_sync
 10786-10829  _classify_pool_anonymity
 10832-10849  _classify_pool_anonymity_bg
   898-920    _claude_chat_sync_metered
  9942-9948   _client_ip
 21940-21967  _clip_prune
 21970-21980  _clip_recfile_for
 22393-22399  _clip_should_velocity
 22022-22104  _clip_to_discord
  3766-3775   _close_ai_session
 22923-22938  _cohost_broadcast
 22908-22909  _cohost_cfg
 22964-22976  _cohost_fire_highlight
 22912-22920  _cohost_gate
 22941-22961  _cohost_highlight
 10434-10436  _conv_messages
  6907-6968   _cookie_alarm_loop
  2110-2111   _cookie_autofetch_info
  2094-2098   _cookie_autorefresh_info
 24801-24823  _cookie_bezug_loop
 24826-24851  _cookie_bezug_runde
  1997-2001   _cookie_header
  9951-9956   _cookie_sicher
  2123-2137   _cookies_selbst_holen
  4096-4098   _create_index_safe
 20826-20940  _crowdsec_status
 20772-20823  _crowdsec_via_lapi
 20676-20694  _cscli_bin
 20703-20716  _cscli_path
  6797-6822   _daily_summary_loop
 20734-20751  _darf_journal_lesen
  3091-3116   _darf_ytdlp_nachschlagen
 11984-12005  _dashboard_adresse
 21336-21359  _db_maintenance_loop
  6766-6794   _db_vacuum_loop
 16260-16284  _detect_foreign_ad
  1587-1598   _diag_path_owner
 17548-17593  _director_finalize
 18633-18640  _director_for
 17497-17545  _director_mark
 22256-22259  _disc_state_get
 22262-22269  _disc_state_set
 21264-21273  _discord_bot_starten
 21227-21238  _discord_einladung_merken
 21276-21280  _discord_invite
 21241-21261  _discord_kontext
 22217-22253  _discord_live_thread
 17700-17712  _discord_notify
 21199-21224  _discord_ops_alert
 22115-22213  _discord_post_user
 21859-21865  _discord_stop
  6825-6902   _disk_alarm_loop
 24726-24775  _disk_autoclean
 24949-24962  _disk_guard_loop
 13853-13860  _drossel_hoeher
 13849-13850  _drossel_stufe
 13863-13871  _drossel_zuruecksetzen
 12161-12163  _dump_all_threads
 24439-24453  _einstellungen_startzeile
 10712-10775  _enrich_proxies_with_geo
  2166-2227   _ensure_cookie_file_netscape
  8947-8950   _ensure_notify_topic
 10956-10993  _ensure_proxy_ready
  8901-8928   _ensure_topic
   740-742    _env_int
   745-747    _env_int_range
 17745-17758  _event_webhook
 12839-12852  _evolution_loop
  5950-5984   _extract_file_payload
  2299-2301   _extract_urls_from_streamurl_node
 20719-20726  _f2b_sudo_hint
 25554-25617  _fatal_vom_botteil
 24348-24363  _fd_grenze_anheben
  4725-4735   _fehler_text
 10613-10631  _fetch_proxy_list
 18299-18327  _fetch_tiktok_room_id
   823-826    _ff_cmd
 18397-18410  _ffprobe_masse
 13682-13687  _find_chromium
  3482-3484   _find_external_recorder
  2304-2306   _find_stream_urls
 12539-12564  _fire_webhooks
  7734-7743   _fork_safe
   931-944    _freeai_chat_sync_metered
 20765-20769  _geo_lookup_ips
  3754-3763   _get_ai_session
  7567-7607   _get_live_info
  2942-2949   _get_resolve_semaphore
  8146-8541   _handle_single_tracking
 24548-24550  _hb
 24553-24570  _hb_while
 13127-13129  _highlight_cfg
 13132-13161  _highlight_observe
 13690-13708  _htmlov_screenshot_cmd
 18004-18014  _httpx_proxy
 12572-12584  _in_quiet_hours
 25382-25393  _init_db_oder_abbruch
 26201-26232  _install_fast_eventloop
  9805-9859   _install_fast_json
 12166-12182  _install_faulthandler
 19381-19390  _intel_ensure_schema
 19433-19468  _intel_index_loop
 19402-19417  _intel_index_one
 19393-19399  _intel_semantic
  5250-5259   _is_authorized
  8032-8053   _is_dead
  2289-2291   _is_hevc
 20754-20756  _is_private_ip
  1806-1813   _is_process_running
  6538-6545   _is_quiet_hours
  1380-1389   _is_upload_window
  4590-4605   _iso
  9959-9965   _ist_lokal
  9894-9907   _json_error_handler
  6760-6761   _kick_broadcaster_id
  7938-7945   _kick_cluster_gefunden
  7894-7935   _kick_cluster_weiter
  6672-6714   _kick_follower_count
  6656-6659   _kick_slug
 11616-11623  _kick_user_token
  7866-7891   _kick_ws_pause
 25370-25379  _kickmod_boot
  4180-4183   _kind_from_filename
 12601-12603  _latest_popularity
  1743-1752   _laufstand
 24909-24946  _laufstand_loop
 24472-24510  _leistung_erheben
 19039-19088  _live_react_loop
 18706-19028  _live_react_worker
  3332-3444   _live_status_aufloesen
 17146-17157  _live_transcript_push
 19030-19037  _live_users
 17596-17640  _living_title_loop
 21502-21574  _local_backup_scan
  9876-9890   _log_5xx
 24513-24545  _log_schleuse_pruefen
   813-820    _log_sicher
 14277-14289  _looks_like_codec_err
 14272-14274  _looks_like_source_expired
  7784-7814   _loop_fehler
 12186-12195  _loop_heartbeat
 24254-24287  _loop_lag_monitor
 24301-24321  _loop_stockung_melden
 24324-24334  _loop_takt_starten
 12198-12271  _loop_watchdog_thread
 17023-17040  _loyalty_add
 17014-17020  _loyalty_get
 17043-17051  _loyalty_top
 12711-12713  _manual_donations_total
  4932-4951   _manual_status
  8055-8056   _mark_dead
 11232-11248  _marketing_loop
 22824-22842  _maybe_handle_command
 25048-25072  _maybe_hype_clip
 21909-21937  _meme_klassifizieren
  4083-4088   _migrate_columns
 23103-23114  _mod_is_exempt
 23117-23122  _mod_warn_first
 23125-23128  _mod_warn_text
 12896-12915  _modlog
 12879-12893  _modlog_schreiben
  1076-1078   _multistream_targets
  3119-3155   _nachschlag_ytdlp
  7746-7747   _nc_create_subprocess_exec
  7750-7751   _nc_create_subprocess_shell
 11553-11570  _news_loop
 12938-12940  _normalize_ingest
  2522-2539   _note_check_duration
  8941-8944   _notify_topic_name
  2712-2718   _offline_ergebnis
  3158-3178   _ohne_url_melden
 17172-17180  _oracle_memories
 17446-17480  _oracle_memorize
 17183-17196  _oracle_persona
 17165-17169  _oracle_recent_text
 13316-13317  _ov_atomic_write
 13307-13309  _ov_bar
 16163-16175  _ov_clip_text
 13312-13313  _ov_oneline
 20431-20460  _overlay_push
 13636-13679  _overlay_render_size
 13007-13011  _overlay_session_reset
 20396-20398  _overlay_src_ok
 16247-16257  _own_invites
 13631-13633  _parse_size
 20948-21028  _parse_ssh_attacks
  7169-7202   _pause_resume_cmd
  2048-2092   _persist_refreshed_cookies
  1951-1983   _pick_checked_pull_proxy
  9996-10009  _pin_auth_value
 10056-10057  _pin_clear_fail
 10036-10039  _pin_locked
 10042-10053  _pin_note_fail
 10012-10033  _pin_ok
 20238-20263  _piper_pick_model
 20323-20374  _piper_say
 12501-12536  _post_json_threaded
 13610-13628  _probe_video_size
  1834-1851   _proc_is_recorder
 10925-10953  _proxy_pool_refresh_loop
  1917-1948   _proxy_report_recording
  8639-8677   _pruefstand_melden
 24383-24394  _pruefung_verworfen
 12151-12153  _prune_stall_dumps
 11302-11472  _public_stats
  2114-2120   _pull_proxy_still
 17716-17742  _push_notify
 10225-10227  _pwa_dir
 10682-10697  _quick_validate_proxy
 12567-12569  _quiet_hours_config
 10190-10223  _rate_guard
 16984-16990  _react_warn
  7654-7693   _reap_proc
  9189-9256   _rec_auto_abschalten
  9136-9186   _rec_frueh_getrennt
  9005-9081   _rec_kategorie_melden
  9084-9133   _rec_totstreak_fortschreiben
  2562-2584   _record_check_outcome
   808-810    _redact_stream_urls
 10852-10922  _refresh_proxy_pool
  2339-2430   _resolve_via_html
  2721-2919   _resolve_via_webcast_api_v2
  2982-3067   _resolve_via_ytdlp
 22433-22562  _resolve_youtube_ingest
  2315-2336   _resolver_stumm
 12990-13001  _restream_active_sources
 13959-14083  _restream_avatar_feeder_start
 14086-14095  _restream_avatar_feeder_stop
 18466-18597  _restream_chat_guardian
 13164-13236  _restream_chat_push
 13293-13302  _restream_chat_push_async
 25277-25320  _restream_durchreicher
 13711-13820  _restream_html_overlay_start
 13823-13836  _restream_html_overlay_stop
 12949-12972  _restream_overlay_files
 19092-19124  _restream_platform_state
 19292-19327  _restream_resume_after_restart
 13267-13290  _restream_status_schreiben
 14143-14215  _restream_tts_enqueue_wav
 13572-13604  _restream_tts_feeder
 13569-13570  _restream_tts_fifo_path
 14098-14125  _restream_tts_start
 14127-14141  _restream_tts_stop
 19130-19289  _restream_verify_loop
 21467-21479  _retention_loop
 21461-21464  _retention_scan
  2669-2671   _room_is_abo
  5988-6105   _run_ai_call
 12294-12307  _run_async_from_flask
 20759-20762  _run_priv
 26189-26197  _run_selfcheck_and_exit
 21482-21493  _s3_client
  8082-8133   _safe_send
  4858-4874   _sample_net_throughput
  2614-2644   _schedule_next_check
 21415-21458  _scheduler_loop
  4091-4093   _schema_pk
 12311-12316  _scraper_session
 23131-23170  _screen_full
 11667-11704  _sec_headers
  2294-2296   _select_stream_from_data_section
 25909-26186  _selfcheck
  8953-8987   _send_live_notice
  1403-1407   _should_defer_upload
 21983-22019  _shrink_for_discord
 10230-10242  _sicheres_ziel
 21295-21333  _sicherheits_erinnerung_loop
 24969-24986  _sign_health_check
 24989-25008  _sign_health_loop
  4608-4633   _sitzung_bestimmen
  7763-7774   _spawn
 26614-26644  _spawn_from_flask
 24397-24403  _speicher_maps
 24406-24421  _speicher_pflegen
 18016-18296  _start_chat_listener
 24366-24380  _start_gesperrt
 12274-12291  _start_loop_watchdog
 11499-11548  _stats_loop
 11478-11481  _stats_output_path
 11484-11496  _stats_write
 20275-20289  _stimme_saubern
 20296-20320  _stimme_schon_gesagt
  8620-8636   _storage_cleanup_loop
 25028-25035  _story_for
  3507-3513   _stream_url_expiry
  3515-3520   _stream_url_ttl
 16210-16217  _streamer_persona_get
 21599-21751  _system_backup
 21760-21790  _system_backup_loop
 12111-12129  _task_auf_bot_schleife
 23944-23960  _telegram_befehlsmenue
  7817-7863   _telegram_polling_fehler
 10634-10673  _test_proxy
 11180-11196  _testpush_resolve_live
  8058-8079   _tg_sprache_setzen
  8860-8870   _tg_topics_load_into_mem
  8857-8858   _tg_topics_path
  8872-8879   _tg_topics_save
  9968-9978   _token_ok
  8882-8886   _topic_forget
 12587-12598  _tracking_max_duration
  4388-4402   _tracking_remove_cleanup
  4419-4431   _tracking_resume_cleanup
  1645-1668   _try_attach_file_handler
 20265-20273  _tts_cleanup
 11156-11160  _tunnel_effective
 24778-24798  _tunnel_lage
 24854-24906  _tunnel_wacht_loop
 19761-19814  _twitch_channel_status
 23173-23318  _twitch_chat_loop
 22275-22288  _twitch_clip_versuchen
 22987-23090  _twitch_eventsub_loop
  1426-1439   _upload_queue_add
  1450-1452   _upload_queue_count
  1409-1418   _upload_queue_load
  1399-1401   _upload_queue_path
  1441-1448   _upload_queue_remove
  1420-1424   _upload_queue_save
  1454-1495   _upload_window_loop
  7627-7634   _uptime_s
 12926-12935  _url_host
  3181-3280   _url_nachschlag
   891-895    _usage_record_claude
 25142-25164  _v37_pause_source
 25106-25116  _v37_restream_restart
 25119-25139  _v37_unpause_source
  7981-8025   _verbindung_verloren
  6717-6748   _viewer_sample_loop
 10060-10063  _wants_html
  7637-7651   _warn_empty_env
 24591-24712  _watchdog_loop
 22708-22716  _wchat_thank_ok
 17784-17814  _whisper_get_model
  7724-7731   _whisper_native_section
 16971-16977  _whisper_pool
 17908-17940  _whisper_segments
 17816-17832  _whisper_stumm
 17835-17905  _whisper_transcribe
 13364-13526  _write_restream_overlay
 13326-13361  _write_restream_overlay_async
 23342-23438  _youtube_api_chat_loop
 19817-19920  _youtube_api_status
 19923-19990  _youtube_channel_status
 23441-23602  _youtube_chat_loop
 22291-22316  _youtube_clip_versuchen
 22568-22581  _youtube_restream_autoconfig
 22584-22608  _youtube_restream_autoconfig_inner
 22675-22703  _youtube_send
 20058-20099  _youtube_set_channel
 22611-22645  _yt_access_token
 22648-22663  _yt_live_chat_id
 22671-22672  _yt_sendrate_cfg
 23321-23336  _yt_timeout
  2966-2967   _ytdlp_detect_available
  2969-2980   _ytdlp_note_result
 12156-12158  _zombie_child_count
 24456-24469  _zustand_kennzahlen
  7503-7527   about
  4299-4303   add_ai_log_entry
  4216-4219   add_archive_entry
  4896-4898   add_archive_rule
  4636-4707   add_recording
  4363-4380   add_tracking
  6108-6141   ai
  3906-3987   ai_chat
  4021-4031   ai_history_append
  4033-4038   ai_history_clear
  4010-4019   ai_history_load
  3995-4008   ai_rate_limit_check
  6170-6178   aireset
 17313-17332  azrael_chat
 23607-23729  brain_cmd
  3523-3528   build_recording_cmd
  4383-4386   bulk_add_trackings
  6971-7030   bulkadd
  8680-8840   check_all_trackings
  4435-4447   claim_live_transition
 16287-16903  class KickModerator
 14292-16050  class RestreamManager
  7948-7978   class _KickClusterSuche
 11039-11081  classify_proxy_anonymity
  6216-6414   cleanup
  5186-5192   cleanup_old_recordings
  4581-4588   clear_recording
 22319-22390  clip_moment
  4848-4851   compute_storage_forecast
  7093-7166   cookies_cmd
  4354-4360   count_trackings_for_chat
  4286-4297   decide_preferred_recorder
  4226-4229   delete_archive_entry
  4900-4902   delete_archive_rule
  5645-5792   diag
 23841-23902  einnahmen_cmd
  4842-4845   find_recordings_by_fingerprint
  4247-4263   finish_recording_attempt
  4407-4409   get_all_active_trackings
  4314-4316   get_all_checks
  4709-4712   get_all_recordings
  4791-4793   get_all_tags_with_counts
  4819-4822   get_annotations_for_recording
  4221-4224   get_archive_entry
  4812-4815   get_bookmarked_recordings
  2154-2159   get_cookie_health
  4779-4785   get_event_log
  4270-4284   get_last_recording_attempt
  3283-3325   get_live_status
  5125-5128   get_manual_recordings
  4827-4830   get_or_compute_inspect_sync
  5227-5230   get_outcome_breakdown
  4798-4801   get_priority_poll_interval
  4265-4268   get_recent_recording_attempts
  4714-4717   get_recording_by_id
  4805-4808   get_recording_note
  3694-3723   get_redis
  4343-4346   get_stats
  5180-5184   get_storage_stats
  4920-4922   get_tiktok_status_distribution
  4449-4458   get_tracking_state
  4404-4405   get_trackings_for_group
  5141-5144   get_trash_recordings
  9316-9784   handle_recording_finished
 23936-23941  hilfe_cmd
  4106-4171   init_db
  4892-4894   list_archive_rules
  5430-5468   live
  8136-8144   live_check_worker
  3778-3817   llm_chat
  3840-3870   llm_chat_sync
  3825-3837   llm_list_models
  4738-4771   log_event
  1768-1801   log_recording_failure
  7316-7365   logs_cmd
 25620-25899  main
  6144-6167   on_ai_media
  7442-7468   on_ai_reply
  7471-7500   on_azrael_mention
  7532-7562   on_callback
 17338-17443  oracle_handle
  7205-7208   pause_tracking
  5240-5245   profile_keyboard
  5383-5427   quelle
  7267-7313   quota
  8543-8617   reaper_loop
  4916-4918   record_tiktok_status
  6183-6213   recstatus
  3725-3733   redis_get_json
  3736-3742   redis_set_json
 23963-23973  report_cmd
 11084-11086  report_proxy_result
  2433-2475   resolve_tiktok_live_stream
  5136-5139   restore_recording
  7211-7214   resume_tracking
  4905-4910   run_archive_rules
 23976-24234  run_bot
 12008-12102  run_flask
  4880-4883   sample_bandwidth_for_active
  4306-4312   save_tiktok_check
  4573-4579   set_recording_file
  4412-4416   set_tracking_paused
  5131-5134   soft_delete_recording
  8993-9003   split_and_send_video
  5293-5335   start
  4231-4245   start_recording_attempt
  6417-6455   stats
  5070-5123   stop_manual_recording
  7217-7264   stoprec
  6641-6649   summary_cmd
  7368-7439   sysres
  5794-5938   teststream
  5337-5378   tiktok
  7033-7090   topusers
  5505-5562   track
  5470-5502   track_exact
  5576-5643   tracklist
  4954-5068   trigger_manual_recording
  4534-4571   try_acquire_recording_lock
  5147-5149   universal_search
 23905-23933  unpause_cmd
  5564-5574   untrack
 23732-23838  update_cmd
  4837-4840   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, beenden, beginnen, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        kategorie, plan
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, uebersicht, vergessen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, ist_telegram_chat, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
