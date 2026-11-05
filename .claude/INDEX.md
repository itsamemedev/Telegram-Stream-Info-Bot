# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10169  GET              /                                                dashboard
 12224  GET              /api/abo/status                                  api_abo_status
 12178  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10957  GET              /api/automation/status                           api_automation_status
 10979  POST             /api/automation/toggle                           api_automation_toggle
 19813  GET              /api/channel/categories                          api_channel_categories
 19819  POST             /api/channel/set                                 api_channel_set
 19666  GET              /api/channels/status                             api_channels_status
 19340  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19323  GET              /api/clips                                       api_clips
 19369  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19241  GET              /api/debug/threads                               api_debug_threads
 12189  GET              /api/events                                      api_events
 11668  GET              /api/events/stream                               api_events_stream
 11495  GET              /api/health                                      api_health
 19282  POST             /api/highlights/config                           api_highlights_config
 10103  POST             /api/login                                       dashboard_login_submit
 12514  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11583  GET              /api/notify/status                               api_notify_status
 11594  POST             /api/notify/test                                 api_notify_test
 12278  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12255  GET              /api/proxy/trend                                 api_proxy_trend
 19389  GET              /api/tts/<fn>                                    api_tts_file
 20166  GET              /api/upload_window                               api_upload_window
 11785  GET              /archive/<int:eid>/download                      archive_download
 11813  GET              /download/<int:recording_id>                     download
 11742  GET              /health                                          health
 19150  GET              /healthz                                         healthz
 10094  GET              /login                                           dashboard_login_page
 10124  GET              /logout                                          dashboard_logout
 10131  GET              /manifest.webmanifest                            pwa_manifest
 20139  GET              /overlay                                         overlay_page
 10155  GET              /pwa-icon-<variant>.png                          pwa_icon
 10141  GET              /sw.js                                           pwa_service_worker
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
   499  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   763  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   645  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   628  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   620  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   807  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   772  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   792  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   679  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
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
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   545  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
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
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
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
   586  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   561  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   973  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1082  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1110  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1130  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   960  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1022  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1009  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   990  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   635  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   630  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   678  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   561  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   888  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   652  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   615  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   588  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   862  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   732  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   821  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   727  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   660  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   440  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   905  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   528  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   783  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   938  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   923  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   484  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   722  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   708  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   691  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   748  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1273  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1394  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1237  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   841  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   737  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
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
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
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
   574  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
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
  2091  /about                  Ueber diesen Bot
   813  /ai                     
  2091  /aireset                KI-Kontext zuruecksetzen
  1222  /ask                    
   914  /assign_role            
   964  /ban                    
  2046  /botstats               
  2091  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2091  /bulkadd                Mehrere User auf einmal tracken · a b c
  2091  /cleanup                Alte Aufnahmen aufraeumen
  1477  /clearwarns             
  2010  /clip                   
  1995  /clipoftheweek          
  1348  /clips                  
  2091  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   869  /create_category        
   840  /create_channel         
   904  /create_group           
   879  /create_role            
   855  /create_voice           
  1100  /daily                  
  2091  /diag                   Vollstaendige Diagnose
  2091  /einnahmen              Einnahmen und Spenden
  1251  /event                  
  1293  /events                 
  1387  /follow                 
  1376  /help                   
   954  /kick                   
  1075  /leaderboard            
  2091  /live                   Live-Status sofort pruefen · @user
  1335  /livenow                
  2091  /logs                   Letzte Fehler aus dem Log
  2091  /pause                  Tracking pausieren · @user
  1363  /post_test              
  1183  /profile                
   986  /purge                  
  2091  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2091  /quota                  Speicher-Quota
  1062  /rank                   
  1323  /recstatus              
   924  /remove_role            
  2091  /report                 Azrael-Sentinel-Wochenreport
   826  /restream_status        
  2091  /resume                 Tracking fortsetzen · @user
   934  /set_channel_perms      
  1029  /setup_community        
  1046  /setup_targets          
  1419  /stats                  
   785  /status                 
  2091  /stoprec                Laufende Aufnahme sauber beenden · @user
  1515  /streaminfo             
  2091  /summary                Tageszusammenfassung
  2091  /sysres                 System-Ressourcen
  2091  /teststream             Recorder-Selbsttest · @user
  2091  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   974  /timeout                
  1487  /topstreamers           
  2091  /topusers               Top-Streamer nach Aufnahmen
   715  /track                  
  2091  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   798  /tracklist              
  1401  /unfollow               
  2091  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   747  /untrack                
  1440  /warn                   
  1463  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2249  on_member_join
  2211  on_message
  2112  on_raw_reaction_add
  2284  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-476    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1592-1643   _award_xp
  1814-1843   _clip_week_leader
  1867-1881   _clipoftheweek_loop
  2400-2462   _community_events_loop
  1549-1571   _dc_client
  1574-1583   _dc_offen
  2502-2537   _disc_automod_check
   403-408    _disc_sprache_setzen
  1646-1694   _discord_ai_automod
   536-575    _discord_automod
  1697-1717   _discord_azrael_reply
  1884-2359   _discord_run_once
   238-296    _discord_start
   299-353    _ensure_discord_invite
  2365-2397   _ensure_error_channel
   424-437    _ensure_rank_roles
   678-692    _ensure_team_roles
  2465-2495   _error_channel_loop
   585-589    _guard
   505-533    _handle_voice_ai
   411-421    _is_admin
  1762-1773   _liveboard_loop
   592-610    _on_level_up
   501-502    _par_chat_id
  1846-1864   _post_clip_of_week
  1776-1794   _post_weekly_digest
   440-466    _provision_base_channels
   469-485    _provision_user_channels
  1315-1408   _reg_betrieb
  1000-1089   _reg_community_setup
  1092-1172   _reg_daily_profil
  1215-1312   _reg_frage_events
   772-828    _reg_info
   946-997    _reg_moderation
  1175-1212   _reg_profil
   895-943    _reg_rollen
   831-892    _reg_server
  1411-1498   _reg_streamer
  1501-1546   _reg_system
   706-769    _reg_tracking
   645-675    _run_tg_handler
   488-498    _tracked_usernames
   155-217    _uebernehmen
  1726-1759   _update_liveboard
  1797-1811   _weekly_digest_loop
   220-223    starte
```

## Top-Level-Symbole in bot.py (542 Funktionen, 2 Klassen)

```
 25054-25076  _abbruch_datenbank_unlesbar
  2662-2663   _abo_key
  2683-2701   _abo_probe_dump
 25172-25188  _abschied_wachen
 25191-25209  _abschluss
 16039-16046  _ad_allowlist
 17038-17044  _agent_for
 17047-17063  _ai_telemetry
 17560-17578  _alert
 21034-21084  _alert_monitor_loop
 21466-21528  _announce_loop
  3548-3558   _anthropic_key
  3565-3567   _anthropic_model
  9786-9789   _arg_int
  2654-2659   _as_dict
 24766-24775  _async_exc_handler
 17741-17763  _audio_tap_cmd
 18321-18380  _audio_tap_melden
 17777-17801  _audio_tap_sammler
  9135-9168   _aufnahme_beim_stopp_sichern
 24015-24017  _aufnahme_deckel
  9171-9189   _aufnahme_platz_frei
 25136-25156  _aufnahmen_abschliessen
 25079-25133  _aufraeumen
  9957-10026  _auth_cookie
  9924-9953   _auth_guard
  1904-1909   _auto_on
 19007-19025  _auto_restream_loop
 13726-13768  _avatar_frames_laden
 22549-22564  _azrael_broadcast_reply
 22449-22471  _azrael_chat_reply
 22421-22446  _azrael_chat_should_reply
 22477-22479  _azrael_gate_cfg
 17068-17082  _azrael_live_state
 20052-20066  _azrael_overlay_state
 17442-17496  _azrael_proactive_loop
 16886-16942  _azrael_reaction_to_chats
 22482-22489  _azrael_reply_all_chats
 22408-22418  _azrael_self_names
 22517-22546  _azrael_send_to
 13687-13723  _azrael_spricht
 14030-14043  _azrael_stimme_stumm
 17088-17109  _azrael_system
 21168-21171  _backup_active
 21249-21262  _backup_loop
 24104-24108  _betrieb
 24839-24848  _brain_crowdsec_snap
 24981-24984  _brain_db_health
 20955-20964  _brain_growth_loop
 10348-10375  _brain_growth_snapshot
  2587-2607   _brain_hint_delay
 24911-24946  _brain_moderation_snap
  6490-6518   _brain_notify
 24987-25009  _brain_recording_snap
 24851-24908  _brain_restream_health
 25012-25025  _brain_tiktok_status_snap
 11647-11664  _browser_push
  6530-6617   _build_daily_summary
 14077-14081  _build_restream_cmd
  5243-5270   _can_stop_tracking
  2017-2039   _capture_set_cookies
 12332-12335  _cfg_get
 12338-12340  _cfg_set
 19774-19809  _channel_set_all
 12915-12918  _chat_connected
 12921-12937  _chat_disconnected
  8778-8789   _chat_is_forum
 18128-18153  _chat_listener_abbauen
 12957-12959  _chat_sanitize
 12900-12912  _chat_stat
 12940-12943  _chat_stats_snapshot
  3866-3878   _check_ai_models_sync
 10630-10673  _classify_pool_anonymity
 10676-10693  _classify_pool_anonymity_bg
   895-917    _claude_chat_sync_metered
  9818-9825   _client_ip
 21612-21639  _clip_prune
 21642-21652  _clip_recfile_for
 22065-22071  _clip_should_velocity
 21694-21776  _clip_to_discord
  3752-3761   _close_ai_session
 22595-22610  _cohost_broadcast
 22580-22581  _cohost_cfg
 22636-22648  _cohost_fire_highlight
 22584-22592  _cohost_gate
 22613-22633  _cohost_highlight
 10278-10280  _conv_messages
  6889-6950   _cookie_alarm_loop
  2107-2108   _cookie_autofetch_info
  2091-2095   _cookie_autorefresh_info
 24473-24495  _cookie_bezug_loop
 24498-24523  _cookie_bezug_runde
  1994-1998   _cookie_header
  2120-2134   _cookies_selbst_holen
  4082-4084   _create_index_safe
 20498-20612  _crowdsec_status
 20444-20495  _crowdsec_via_lapi
 20348-20366  _cscli_bin
 20375-20388  _cscli_path
  6779-6804   _daily_summary_loop
 20406-20423  _darf_journal_lesen
  3077-3102   _darf_ytdlp_nachschlagen
 11828-11849  _dashboard_adresse
 21008-21031  _db_maintenance_loop
  6748-6776   _db_vacuum_loop
 16062-16086  _detect_foreign_ad
  1584-1595   _diag_path_owner
 17347-17392  _director_finalize
 18310-18317  _director_for
 17296-17344  _director_mark
 21928-21931  _disc_state_get
 21934-21941  _disc_state_set
 20936-20945  _discord_bot_starten
 20899-20910  _discord_einladung_merken
 20948-20952  _discord_invite
 20913-20933  _discord_kontext
 21889-21925  _discord_live_thread
 17499-17511  _discord_notify
 20871-20896  _discord_ops_alert
 21787-21885  _discord_post_user
 21531-21537  _discord_stop
  6807-6884   _disk_alarm_loop
 24398-24447  _disk_autoclean
 24621-24634  _disk_guard_loop
 13665-13672  _drossel_hoeher
 13661-13662  _drossel_stufe
 13675-13683  _drossel_zuruecksetzen
 12005-12007  _dump_all_threads
 24111-24125  _einstellungen_startzeile
 10556-10619  _enrich_proxies_with_geo
  2163-2224   _ensure_cookie_file_netscape
  8837-8840   _ensure_notify_topic
 10800-10837  _ensure_proxy_ready
  8791-8818   _ensure_topic
   737-739    _env_int
   742-744    _env_int_range
 17544-17557  _event_webhook
 12683-12696  _evolution_loop
  5932-5966   _extract_file_payload
  2296-2298   _extract_urls_from_streamurl_node
 20391-20398  _f2b_sudo_hint
 25212-25275  _fatal_vom_botteil
 24020-24035  _fd_grenze_anheben
  4707-4717   _fehler_text
 10457-10475  _fetch_proxy_list
 18097-18125  _fetch_tiktok_room_id
   820-823    _ff_cmd
 13494-13499  _find_chromium
  3468-3470   _find_external_recorder
  2301-2303   _find_stream_urls
 12383-12408  _fire_webhooks
  7716-7725   _fork_safe
   928-941    _freeai_chat_sync_metered
 20437-20441  _geo_lookup_ips
  3740-3749   _get_ai_session
  7549-7589   _get_live_info
  2928-2935   _get_resolve_semaphore
  8041-8431   _handle_single_tracking
 24220-24222  _hb
 24225-24242  _hb_while
 12971-12973  _highlight_cfg
 12976-13005  _highlight_observe
 13502-13520  _htmlov_screenshot_cmd
 17803-17813  _httpx_proxy
 12416-12428  _in_quiet_hours
 25040-25051  _init_db_oder_abbruch
 25859-25890  _install_fast_eventloop
  9681-9735   _install_fast_json
 12010-12026  _install_faulthandler
 19053-19062  _intel_ensure_schema
 19105-19140  _intel_index_loop
 19074-19089  _intel_index_one
 19065-19071  _intel_semantic
  5232-5241   _is_authorized
  7927-7948   _is_dead
  2286-2288   _is_hevc
 20426-20428  _is_private_ip
  1803-1810   _is_process_running
  6520-6527   _is_quiet_hours
  1377-1386   _is_upload_window
  4572-4587   _iso
  9770-9783   _json_error_handler
  6742-6743   _kick_broadcaster_id
  6654-6696   _kick_follower_count
  6638-6641   _kick_slug
 11460-11467  _kick_user_token
  7848-7873   _kick_ws_pause
 25028-25037  _kickmod_boot
  4162-4165   _kind_from_filename
 12445-12447  _latest_popularity
  1740-1749   _laufstand
 24581-24618  _laufstand_loop
 24144-24182  _leistung_erheben
 18716-18765  _live_react_loop
 18383-18705  _live_react_worker
  3318-3430   _live_status_aufloesen
 16945-16956  _live_transcript_push
 18707-18714  _live_users
 17395-17439  _living_title_loop
 21174-21246  _local_backup_scan
  9752-9766   _log_5xx
 24185-24217  _log_schleuse_pruefen
   810-817    _log_sicher
 14089-14101  _looks_like_codec_err
 14084-14086  _looks_like_source_expired
  7766-7796   _loop_fehler
 12030-12039  _loop_heartbeat
 23926-23959  _loop_lag_monitor
 23973-23993  _loop_stockung_melden
 23996-24006  _loop_takt_starten
 12042-12115  _loop_watchdog_thread
 16822-16839  _loyalty_add
 16813-16819  _loyalty_get
 16842-16850  _loyalty_top
 12555-12557  _manual_donations_total
  4914-4933   _manual_status
  7950-7951   _mark_dead
 11076-11092  _marketing_loop
 22496-22514  _maybe_handle_command
 24720-24744  _maybe_hype_clip
 21581-21609  _meme_klassifizieren
  4069-4074   _migrate_columns
 22775-22786  _mod_is_exempt
 22789-22794  _mod_warn_first
 22797-22800  _mod_warn_text
 12740-12759  _modlog
 12723-12737  _modlog_schreiben
  1073-1075   _multistream_targets
  3105-3141   _nachschlag_ytdlp
  7728-7729   _nc_create_subprocess_exec
  7732-7733   _nc_create_subprocess_shell
 11397-11414  _news_loop
 12782-12784  _normalize_ingest
  2518-2535   _note_check_duration
  8831-8834   _notify_topic_name
  3144-3164   _ohne_url_melden
 16971-16979  _oracle_memories
 17245-17279  _oracle_memorize
 16982-16995  _oracle_persona
 16964-16968  _oracle_recent_text
 13128-13129  _ov_atomic_write
 13119-13121  _ov_bar
 15965-15977  _ov_clip_text
 13124-13125  _ov_oneline
 20103-20132  _overlay_push
 13448-13491  _overlay_render_size
 12851-12855  _overlay_session_reset
 20068-20070  _overlay_src_ok
 16049-16059  _own_invites
 13443-13445  _parse_size
 20620-20700  _parse_ssh_attacks
  7151-7184   _pause_resume_cmd
  2045-2089   _persist_refreshed_cookies
  1948-1980   _pick_checked_pull_proxy
  9854-9867   _pin_auth_value
  9913-9914   _pin_clear_fail
  9893-9896   _pin_locked
  9899-9910   _pin_note_fail
  9870-9890   _pin_ok
 19910-19935  _piper_pick_model
 19995-20046  _piper_say
 12345-12380  _post_json_threaded
 13422-13440  _probe_video_size
  1831-1848   _proc_is_recorder
 10769-10797  _proxy_pool_refresh_loop
  1914-1945   _proxy_report_recording
  8529-8567   _pruefstand_melden
 24055-24066  _pruefung_verworfen
 11995-11997  _prune_stall_dumps
 11146-11316  _public_stats
  2111-2117   _pull_proxy_still
 17515-17541  _push_notify
 10073-10075  _pwa_dir
 10526-10541  _quick_validate_proxy
 12411-12413  _quiet_hours_config
 10038-10071  _rate_guard
 16783-16789  _react_warn
  7636-7675   _reap_proc
  9065-9132   _rec_auto_abschalten
  9012-9062   _rec_frueh_getrennt
  8895-8957   _rec_kategorie_melden
  8960-9009   _rec_totstreak_fortschreiben
  2558-2580   _record_check_outcome
   805-807    _redact_stream_urls
 10696-10766  _refresh_proxy_pool
  2335-2426   _resolve_via_html
  2708-2905   _resolve_via_webcast_api_v2
  2968-3053   _resolve_via_ytdlp
 22105-22234  _resolve_youtube_ingest
  2312-2332   _resolver_stumm
 12834-12845  _restream_active_sources
 13771-13895  _restream_avatar_feeder_start
 13898-13907  _restream_avatar_feeder_stop
 18156-18274  _restream_chat_guardian
 13008-13080  _restream_chat_push
 13105-13114  _restream_chat_push_async
 24949-24978  _restream_durchreicher
 13523-13632  _restream_html_overlay_start
 13635-13648  _restream_html_overlay_stop
 12793-12816  _restream_overlay_files
 18769-18801  _restream_platform_state
 18969-19004  _restream_resume_after_restart
 13955-14027  _restream_tts_enqueue_wav
 13384-13416  _restream_tts_feeder
 13381-13382  _restream_tts_fifo_path
 13910-13937  _restream_tts_start
 13939-13953  _restream_tts_stop
 18807-18966  _restream_verify_loop
 21139-21151  _retention_loop
 21133-21136  _retention_scan
  2665-2667   _room_is_abo
  5970-6087   _run_ai_call
 12138-12151  _run_async_from_flask
 20431-20434  _run_priv
 25847-25855  _run_selfcheck_and_exit
 21154-21165  _s3_client
  7977-8028   _safe_send
  4840-4856   _sample_net_throughput
  2610-2640   _schedule_next_check
 21087-21130  _scheduler_loop
  4077-4079   _schema_pk
 12155-12160  _scraper_session
 22803-22842  _screen_full
 11511-11548  _sec_headers
  2291-2293   _select_stream_from_data_section
 25567-25844  _selfcheck
  8843-8877   _send_live_notice
  1400-1404   _should_defer_upload
 21655-21691  _shrink_for_discord
 10078-10090  _sicheres_ziel
 20967-21005  _sicherheits_erinnerung_loop
 24641-24658  _sign_health_check
 24661-24680  _sign_health_loop
  4590-4615   _sitzung_bestimmen
  7745-7756   _spawn
 26272-26302  _spawn_from_flask
 24069-24075  _speicher_maps
 24078-24093  _speicher_pflegen
 17815-18094  _start_chat_listener
 24038-24052  _start_gesperrt
 12118-12135  _start_loop_watchdog
 11343-11392  _stats_loop
 11322-11325  _stats_output_path
 11328-11340  _stats_write
 19947-19961  _stimme_saubern
 19968-19992  _stimme_schon_gesagt
  8510-8526   _storage_cleanup_loop
 24700-24707  _story_for
  3493-3499   _stream_url_expiry
  3501-3506   _stream_url_ttl
 16012-16019  _streamer_persona_get
 21271-21423  _system_backup
 21432-21462  _system_backup_loop
 11955-11973  _task_auf_bot_schleife
 23616-23632  _telegram_befehlsmenue
  7799-7845   _telegram_polling_fehler
 10478-10517  _test_proxy
 11024-11040  _testpush_resolve_live
  7953-7974   _tg_sprache_setzen
  8750-8760   _tg_topics_load_into_mem
  8747-8748   _tg_topics_path
  8762-8769   _tg_topics_save
  9828-9836   _token_ok
  8772-8776   _topic_forget
 12431-12442  _tracking_max_duration
  4370-4384   _tracking_remove_cleanup
  4401-4413   _tracking_resume_cleanup
  1642-1665   _try_attach_file_handler
 19937-19945  _tts_cleanup
 11000-11004  _tunnel_effective
 24450-24470  _tunnel_lage
 24526-24578  _tunnel_wacht_loop
 19433-19486  _twitch_channel_status
 22845-22990  _twitch_chat_loop
 21947-21960  _twitch_clip_versuchen
 22659-22762  _twitch_eventsub_loop
  1423-1436   _upload_queue_add
  1447-1449   _upload_queue_count
  1406-1415   _upload_queue_load
  1396-1398   _upload_queue_path
  1438-1445   _upload_queue_remove
  1417-1421   _upload_queue_save
  1451-1492   _upload_window_loop
  7609-7616   _uptime_s
 12770-12779  _url_host
  3167-3266   _url_nachschlag
   888-892    _usage_record_claude
 24814-24836  _v37_pause_source
 24778-24788  _v37_restream_restart
 24791-24811  _v37_unpause_source
  7876-7920   _verbindung_verloren
  6699-6730   _viewer_sample_loop
  9917-9920   _wants_html
  7619-7633   _warn_empty_env
 24263-24384  _watchdog_loop
 22380-22388  _wchat_thank_ok
 17583-17613  _whisper_get_model
  7706-7713   _whisper_native_section
 16770-16776  _whisper_pool
 17707-17739  _whisper_segments
 17615-17631  _whisper_stumm
 17634-17704  _whisper_transcribe
 13176-13338  _write_restream_overlay
 13138-13173  _write_restream_overlay_async
 23014-23110  _youtube_api_chat_loop
 19489-19592  _youtube_api_status
 19595-19662  _youtube_channel_status
 23113-23274  _youtube_chat_loop
 21963-21988  _youtube_clip_versuchen
 22240-22253  _youtube_restream_autoconfig
 22256-22280  _youtube_restream_autoconfig_inner
 22347-22375  _youtube_send
 19730-19771  _youtube_set_channel
 22283-22317  _yt_access_token
 22320-22335  _yt_live_chat_id
 22343-22344  _yt_sendrate_cfg
 22993-23008  _yt_timeout
  2952-2953   _ytdlp_detect_available
  2955-2966   _ytdlp_note_result
 12000-12002  _zombie_child_count
 24128-24141  _zustand_kennzahlen
  7485-7509   about
  4281-4285   add_ai_log_entry
  4198-4201   add_archive_entry
  4878-4880   add_archive_rule
  4618-4689   add_recording
  4345-4362   add_tracking
  6090-6123   ai
  3892-3973   ai_chat
  4007-4017   ai_history_append
  4019-4024   ai_history_clear
  3996-4005   ai_history_load
  3981-3994   ai_rate_limit_check
  6152-6160   aireset
 17112-17131  azrael_chat
 23279-23401  brain_cmd
  3509-3514   build_recording_cmd
  4365-4368   bulk_add_trackings
  6953-7012   bulkadd
  8570-8730   check_all_trackings
  4417-4429   claim_live_transition
 16089-16702  class KickModerator
 14104-15852  class RestreamManager
 10883-10925  classify_proxy_anonymity
  6198-6396   cleanup
  5168-5174   cleanup_old_recordings
  4563-4570   clear_recording
 21991-22062  clip_moment
  4830-4833   compute_storage_forecast
  7075-7148   cookies_cmd
  4336-4342   count_trackings_for_chat
  4268-4279   decide_preferred_recorder
  4208-4211   delete_archive_entry
  4882-4884   delete_archive_rule
  5627-5774   diag
 23513-23574  einnahmen_cmd
  4824-4827   find_recordings_by_fingerprint
  4229-4245   finish_recording_attempt
  4389-4391   get_all_active_trackings
  4296-4298   get_all_checks
  4691-4694   get_all_recordings
  4773-4775   get_all_tags_with_counts
  4801-4804   get_annotations_for_recording
  4203-4206   get_archive_entry
  4794-4797   get_bookmarked_recordings
  2151-2156   get_cookie_health
  4761-4767   get_event_log
  4252-4266   get_last_recording_attempt
  3269-3311   get_live_status
  5107-5110   get_manual_recordings
  4809-4812   get_or_compute_inspect_sync
  5209-5212   get_outcome_breakdown
  4780-4783   get_priority_poll_interval
  4247-4250   get_recent_recording_attempts
  4696-4699   get_recording_by_id
  4787-4790   get_recording_note
  3680-3709   get_redis
  4325-4328   get_stats
  5162-5166   get_storage_stats
  4902-4904   get_tiktok_status_distribution
  4431-4440   get_tracking_state
  4386-4387   get_trackings_for_group
  5123-5126   get_trash_recordings
  9192-9660   handle_recording_finished
 23608-23613  hilfe_cmd
  4092-4153   init_db
  4874-4876   list_archive_rules
  5412-5450   live
  8031-8039   live_check_worker
  3764-3803   llm_chat
  3826-3856   llm_chat_sync
  3811-3823   llm_list_models
  4720-4753   log_event
  1765-1798   log_recording_failure
  7298-7347   logs_cmd
 25278-25557  main
  6126-6149   on_ai_media
  7424-7450   on_ai_reply
  7453-7482   on_azrael_mention
  7514-7544   on_callback
 17137-17242  oracle_handle
  7187-7190   pause_tracking
  5222-5227   profile_keyboard
  5365-5409   quelle
  7249-7295   quota
  8433-8507   reaper_loop
  4898-4900   record_tiktok_status
  6165-6195   recstatus
  3711-3719   redis_get_json
  3722-3728   redis_set_json
 23635-23645  report_cmd
 10928-10930  report_proxy_result
  2429-2471   resolve_tiktok_live_stream
  5118-5121   restore_recording
  7193-7196   resume_tracking
  4887-4892   run_archive_rules
 23648-23906  run_bot
 11852-11946  run_flask
  4862-4865   sample_bandwidth_for_active
  4288-4294   save_tiktok_check
  4555-4561   set_recording_file
  4394-4398   set_tracking_paused
  5113-5116   soft_delete_recording
  8883-8893   split_and_send_video
  5275-5317   start
  4213-4227   start_recording_attempt
  6399-6437   stats
  5052-5105   stop_manual_recording
  7199-7246   stoprec
  6623-6631   summary_cmd
  7350-7421   sysres
  5776-5920   teststream
  5319-5360   tiktok
  7015-7072   topusers
  5487-5544   track
  5452-5484   track_exact
  5558-5625   tracklist
  4936-5050   trigger_manual_recording
  4516-4553   try_acquire_recording_lock
  5129-5131   universal_search
 23577-23605  unpause_cmd
  5546-5556   untrack
 23404-23510  update_cmd
  4819-4822   update_recording_fingerprint
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
beobachtungsdienst.py  grafana_jetzt, grafana_lage, grafana_unit, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
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
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
envdatei.py            class EnvdateiFehler, lesen, main, setzen
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
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
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
meldetakt.py           melden, zuruecksetzen, zusatz
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
schema.py              anlegen, create_schema, index_sicher, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid
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
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
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
